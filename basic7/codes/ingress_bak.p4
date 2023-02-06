/*************************************************************************
**************  I N G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyIngress(inout headers hdr,
                  inout metadata meta,
                  inout standard_metadata_t standard_metadata) {

    // 1. Declare reigsters
    register<bit<16>>(100000) flows_vector;
    //register<bit<16>>(10000) hashID_vector;
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

// Classes table for classified flows
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
      // We can also add flags check conditions
      if(hdr.ipv4.protocol ==6){

        // 1. Take hash of flow
        hash(meta.flowID,
          HashAlgorithm.crc16,
          (bit<16>)0,
          {hdr.ipv4.srcAddr,
          hdr.ipv4.dstAddr,
          hdr.tcp.srcPort,
          hdr.tcp.dstPort,
          hdr.ipv4.protocol},
          (bit<16>)1000);

        // 2. Chekc garbage flows
        if (meta.flowID != 524){

          // 3. calculate packet counter for flow
          packet_counter_reg.read(meta.packet_counter, (bit<32>)meta.flowID);
          meta.packet_counter = meta.packet_counter + 1;

          meta.packetSize = hdr.ipv4.totalLen - 40;

          //log_msg(" INFO FlowID : {} packetCounter : {} Size : {} ", {meta.flowID, meta.packet_counter, hdr.ipv4.totalLen - 40});

          // 4. Check if the flow is already classified
          classifiedFlows.read(meta.classID, (bit<32>)meta.flowID);
          log_msg(" INFO FlowID : {} ClassID : {} packetCounter : {} ", {meta.flowID, meta.classID, meta.packet_counter});

          if (meta.packet_counter < 4){
              flows_vector.write((bit<32>)(meta.flowID*4+meta.packet_counter), meta.packetSize);
              packet_counter_reg.write((bit<32>)meta.flowID, meta.packet_counter);
          }

          // 5. If threshold reaches then read sizes from register
          if (meta.packet_counter == 4){
              flows_vector.write((bit<32>)(meta.flowID*4+meta.packet_counter), meta.packetSize);
              flows_vector.read(meta.firstPacketSize, (bit<32>)(meta.flowID*4+1));
              flows_vector.read(meta.secondPacketSize, (bit<32>)(meta.flowID*4+2));
              flows_vector.read(meta.thirdPacketSize, (bit<32>)(meta.flowID*4+3));
              flows_vector.read(meta.fourthPacketSize, (bit<32>)(meta.flowID*4+4));

              // Troubleshooting
              log_msg(" INFO FlowID : {} 1stPacket : {} 2ndPacket : {} 3rdPacket : {} 4thPacket : {}",
              { meta.flowID, meta.firstPacketSize, meta.secondPacketSize, meta.thirdPacketSize, meta.fourthPacketSize});

              // 6. Apply classification tables
              //Match packet sizes
              feature1_exact.apply();
              feature2_exact.apply();
              feature3_exact.apply();
              feature4_exact.apply();

              // Apply actions if the size matches
              ipv4_exact.apply();
              packet_counter_reg.write((bit<32>)meta.flowID, meta.packet_counter);

              // Set port to meta in action and save class ID to register
              // When we successfully aply ipv4_exact table then we set the metaClassPort from action
              meta.classID = meta.currentClassPort;
              classifiedFlows.write((bit<32>)meta.flowID, meta.classID);  // We store classified flows with output port

            }

            if (meta.packet_counter > 4 && meta.classID != 0){
                hdr.tcp.clasID = meta.classID;             // Class ID will act as match that can direct the node to forward on dedicated port
                // Apply class on classiifed flows only
                classes_forward.apply();
                packet_counter_reg.write((bit<32>)meta.flowID, meta.packet_counter);

            }


        } // Check garbage flows
      } // TCP check
    } // IP validity condition check
} // apply
} // Ingress control
