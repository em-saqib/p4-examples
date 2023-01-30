/*************************************************************************
**************  I N G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyIngress(inout headers hdr,
                  inout metadata meta,
                  inout standard_metadata_t standard_metadata) {

    // 1. Declare reigsters
    register<bit<16>>(10000) flows_vector;
    register<bit<16>>(1000) hashID_vector;
    register<bit<16>>(1000) packet_counter_reg;
    register<bit<16>>(1000) classifiedFlows;



    action drop() {
        mark_to_drop(standard_metadata);
    }

    action ipv4_forward(macAddr_t dstAddr, egressSpec_t port) {
        standard_metadata.egress_spec = port;
        hdr.ethernet.srcAddr = hdr.ethernet.dstAddr;
        hdr.ethernet.dstAddr = dstAddr;
        meta.currentClassPort = (bit<16>)port;
        }

action set_actionselect1(bit<14> featurevalue1){
    meta.action_select1 = featurevalue1 ;
}

action set_actionselect2(bit<14> featurevalue2){
    meta.action_select2 = featurevalue2 ;
}

action set_actionselect3(bit<14> featurevalue3){
    meta.action_select3 = featurevalue3 ;
}

action set_actionselect4(bit<14> featurevalue4){
    meta.action_select4 = featurevalue4 ;
}

action class_forward(macAddr_t dstAddr, egressSpec_t port) {
    standard_metadata.egress_spec = port;
    hdr.ethernet.srcAddr = hdr.ethernet.dstAddr;
    hdr.ethernet.dstAddr = dstAddr;
    }

// feature table 1st packet size
table feature1_exact{
key = {
    //hdr.ipv4.totalLen : range ;
    meta.firstPacketSize : range ;
        }
        actions = {
            NoAction;
            set_actionselect1;
                }
                    size = 1024;
}

// feature table 2nd packet size
table feature2_exact{
key = {
    meta.secondPacketSize : range ;
        }
        actions = {
            NoAction;
            set_actionselect2;
                }
                    size = 1024;
}

// feature table 3rd packet size
table feature3_exact{
key = {
    meta.thirdPacketSize : range ;
        }
        actions = {
            NoAction;
            set_actionselect3;
                }
                    size = 1024;
}

// feature table 4th packet size
table feature4_exact{
key = {
    meta.fourthPacketSize : range ;
        }
        actions = {
            NoAction;
            set_actionselect4;
                }
                    size = 1024;
}


// decision table match metadata
    table ipv4_exact {
        key = {
            meta.action_select1: range;
            meta.action_select2: range;
            meta.action_select3: range;
            meta.action_select4: range;
                }
 actions = {
    ipv4_forward;
    drop;
    NoAction;
        }
        size = 1024;
        default_action = drop();
    }

// classes table for classified flows
    table classes_forward {
        key = {
          hdr.tcp.clasID : exact;
              }

    actions = {
        class_forward;
        drop;
        NoAction;
            }
            size = 1024;
            default_action = drop();
        }

apply {
    if (hdr.ipv4.isValid() ) {
        //feature1_exact.apply();
            if(hdr.ipv4.protocol ==6) {


                // 2. Take hash of flow
                hash(meta.flowID,
                    HashAlgorithm.crc16,
                    (bit<16>)0,
                    {hdr.ipv4.srcAddr,
                    hdr.ipv4.dstAddr,
                    hdr.tcp.srcPort,
                    hdr.tcp.dstPort,
                    hdr.ipv4.protocol},
                    (bit<16>)1000);

                    // 3. Read packet size and keep in metadata
                    meta.packetSize = hdr.ipv4.totalLen - 40;

                    // 4. save packet sizes to register of particular flow
                    packet_counter_reg.read(meta.packet_counter, (bit<32>)meta.flowID);
                    meta.packet_counter = meta.packet_counter + 1;
                    //log_msg(" INFO FlowID : {} PackCounter : {}", {meta.flowID, meta.packet_counter});

                    if (meta.packet_counter < 4)
                    {
                        flows_vector.write((bit<32>)(meta.flowID*4+meta.packet_counter), meta.packetSize);
                        packet_counter_reg.write((bit<32>)meta.flowID, meta.packet_counter);
                    }

                    // 5. If threshold reaches then read sizes from register
                    if (meta.packet_counter == 4){

                        flows_vector.write((bit<32>)(meta.flowID*4+meta.packet_counter), meta.packetSize);
                        packet_counter_reg.write((bit<32>)meta.flowID, meta.packet_counter);

                        flows_vector.read(meta.firstPacketSize, (bit<32>)(meta.flowID*4+1));
                        flows_vector.read(meta.secondPacketSize, (bit<32>)(meta.flowID*4+2));
                        flows_vector.read(meta.thirdPacketSize, (bit<32>)(meta.flowID*4+3));
                        flows_vector.read(meta.thirdPacketSize, (bit<32>)(meta.flowID*4+4));

                        //log_msg(" INFO FlowID : {} 1stPacket : {} 2ndPacket : {} 3rdPacket : {}",
                        // {meta.flowID, meta.firstPacketSize, meta.secondPacketSize, meta.thirdPacketSize});

                        // 7. Match packet sizes
                        feature1_exact.apply();
                        feature2_exact.apply();
                        feature3_exact.apply();
                        feature4_exact.apply();

                        // Apply actions if the size matches
                        ipv4_exact.apply();

                        // Set port to meta in action and save class ID to register
                        // When we successfully aply ipv4_exact table then we set the metaClassPort from action
                        meta.classID = meta.currentClassPort;
                        classifiedFlows.write((bit<32>)meta.flowID, meta.classID);  // We store classified flows with output port
                    }

                    // Directly forward packet if the flow is classifed
                    // If counter reaches limit and flow is classified, add boolean condition
                    if (meta.packet_counter > 4){

                        // This counter is for troyublshooting purpose to counts packets for each flow
                        packet_counter_reg.write((bit<32>)meta.flowID, meta.packet_counter);

                        // Check if the packet already classiifed and forward it to corresponding port
                        classifiedFlows.read(meta.classID, (bit<32>)meta.flowID);
                        if (meta.classID != 0){
                            hdr.tcp.clasID = meta.classID;
                            // Apply class on classiifed flows only
                            classes_forward.apply();
                            log_msg(" INFO Flow_ID : {} Class_ID : {} ForwardedPort {}", {meta.flowID, meta.classID, hdr.tcp.clasID});
                        }
                    }

}
}


} // Apply block end here
} // Ingress block end here
