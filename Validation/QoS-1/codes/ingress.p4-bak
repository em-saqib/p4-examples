
/*************************************************************************
**************  I N G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

#include "telemet.p4"
#include "classification.p4"

/*Queue with index 0 is the bottom one, with lowest priority*/
register<bit<32>>(8) queue_bound;
register<bit<32>>(8) queue_delay;
register<bit<32>>(8) procTime_reg;

control MyIngress(inout headers hdr,
                  inout local_metadata_t metadata,
                  inout standard_metadata_t standard_metadata) {


    action drop() {
        mark_to_drop(standard_metadata);
    }

    action ipv4_forward(macAddr_t dst_addr, egressSpec_t port) {
        standard_metadata.egress_spec = port;
        hdr.ethernet.src_addr = hdr.ethernet.dst_addr;
        hdr.ethernet.dst_addr = dst_addr;
        hdr.ipv4.ttl = hdr.ipv4.ttl - 1;
    }


    table ipv4_lpm {
        key = {
            hdr.ipv4.dst_addr: lpm;
        }
        actions = {
            ipv4_forward;
            drop;
            NoAction;
        }
        size = 1024;
        default_action = drop();
    }


    apply {
        if (hdr.ipv4.isValid()) {

            if(hdr.ipv4.protocol ==6) {

            // INT + Classification + Queueing + Admission Control

            // 1. Add INT Header
            process_int.apply(hdr, metadata);

            // 2. Apply Classification Process
            classification.apply(hdr, metadata, standard_metadata);


            // 3. Apply Multi-Priority Queueing
            standard_metadata.priority = (bit<3>)hdr.int_header.class;

            queue_delay.read(metadata.current_queue_delay, (bit<32>)standard_metadata.priority); // read the delay of particular queue
            procTime_reg.read(metadata.procTime, 0);

            //log_msg(" INFO FlowID :{} ClassID : {} Priority : {} PacketCounter : {} Latency : {} qDelay : {} procTime : {}", {metadata.flowID, hdr.int_header.class, standard_metadata.priority, metadata.packet_counter, hdr.int_header.latency, metadata.current_queue_delay, metadata.procTime});
            log_msg(" INFO ClassID : {} PacketCounter : {} Latency : {} qDelay : {} ", {hdr.int_header.class, metadata.packet_counter, hdr.int_header.latency, metadata.current_queue_delay});

            // 4. Admission Control Policyy
            if (hdr.int_header.latency > metadata.current_queue_delay){
                ipv4_lpm.apply();
            }
            }
        }
    }
}


/*************************************************************************
****************  E G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyEgress(inout headers hdr,
                 inout local_metadata_t metadata,
                 inout standard_metadata_t standard_metadata) {
    apply {

          // Store queueing data into metadata
          //metadata.queueing_metadata.enq_timestamp = standard_metadata.enq_timestamp;
          //metadata.queueing_metadata.enq_qdepth = standard_metadata.enq_qdepth;
          //metadata.queueing_metadata.deq_timedelta = standard_metadata.deq_timedelta;
          //metadata.queueing_metadata.deq_qdepth = standard_metadata.deq_qdepth;
          //metadata.q_delay = (bit<32>)standard_metadata.deq_timedelta;

          bit<3> qid = standard_metadata.priority;
          metadata.procTime = (bit<32>)standard_metadata.egress_global_timestamp - (bit<32>)standard_metadata.ingress_global_timestamp;
          procTime_reg.write((bit<32>)qid, metadata.procTime);
          queue_delay.write((bit<32>)qid, standard_metadata.deq_timedelta);

          //log_msg(" INFO ClassID : {} PacketCounter : {} Latency : {} qDelay : {} ", {hdr.int_header.class, hdr.int_header.c_p_counter, hdr.int_header.latency, standard_metadata.deq_timedelta});

          // Update Latency by substracting queue delay
          if (hdr.int_header.latency > metadata.current_queue_delay){
            hdr.int_header.latency = hdr.int_header.latency - (bit<32>)metadata.current_queue_delay;   // Process time included queueing delay
          }


     }
}
