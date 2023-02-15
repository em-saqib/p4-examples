
/*************************************************************************
**************  I N G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

#include "telemet.p4"

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

            // 1. Classification process
            // 3. Embed class id and QoS requirments into packet's header
            if (hdr.ipv4.len == 41){
                metadata.class_id = 1;
                metadata.t_latency = 1000;
                metadata.r_latency = 100;
                metadata.priority = 1;
            }
            if (hdr.ipv4.len == 42){
                metadata.class_id = 2;
                metadata.t_latency = 2000;
                metadata.r_latency = 2000;
                metadata.priority = 2;
            }
            process_int.apply(hdr, metadata);

            // 3. Admission control policity
            //    a. Estimate queueing delay
            if (metadata.q_delay < hdr.int_header.r_latency){

                // 4. Priority based queueing

                ipv4_lpm.apply();
                log_msg(" INFO Class : {} T_Latency : {} R_Latency : {} Priority : {} ", {hdr.int_header.class, hdr.int_header.t_latency, hdr.int_header.r_latency, hdr.int_header.priority});


            }





        }
    }
}
