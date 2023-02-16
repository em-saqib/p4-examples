
/*************************************************************************
**************  I N G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

#include "telemet.p4"

control MyIngress(inout headers hdr,
                  inout local_metadata_t metadata,
                  inout standard_metadata_t standard_metadata) {

    /*Queue with index 0 is the bottom one, with lowest priority*/
    register<bit<32>>(8) queue_bound;

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


                metadata.rank = (bit<32>)hdr.int_header.class;
                queue_bound.read(metadata.current_queue_bound, 0);
                if ((metadata.current_queue_bound <= metadata.rank)) {
                    standard_metadata.priority = (bit<3>)0;
                    queue_bound.write(0, metadata.rank);
                } else {
                    queue_bound.read(metadata.current_queue_bound, 1);
                    if ((metadata.current_queue_bound <= metadata.rank)) {
                        standard_metadata.priority = (bit<3>)1;
                        queue_bound.write(1, metadata.rank);
                    } else {
                        queue_bound.read(metadata.current_queue_bound, 2);
                        if ((metadata.current_queue_bound <= metadata.rank)) {
                            standard_metadata.priority = (bit<3>)2;
                            queue_bound.write(2, metadata.rank);
                        } else {
                            queue_bound.read(metadata.current_queue_bound, 3);
                            if ((metadata.current_queue_bound <= metadata.rank)) {
                                standard_metadata.priority = (bit<3>)3;
                                queue_bound.write(3, metadata.rank);
                            } else {
                                queue_bound.read(metadata.current_queue_bound, 4);
                                if ((metadata.current_queue_bound <= metadata.rank)) {
                                    standard_metadata.priority = (bit<3>)4;
                                    queue_bound.write(4, metadata.rank);
                                } else {
                                    queue_bound.read(metadata.current_queue_bound, 5);
                                    if ((metadata.current_queue_bound <= metadata.rank)) {
                                        standard_metadata.priority = (bit<3>)5;
                                        queue_bound.write(5, metadata.rank);
                                    } else {
                                        queue_bound.read(metadata.current_queue_bound, 6);
                                        if ((metadata.current_queue_bound <= metadata.rank)) {
                                            standard_metadata.priority = (bit<3>)6;
                                            queue_bound.write(6, metadata.rank);
                                        } else {
                                            standard_metadata.priority = (bit<3>)7;
                                            queue_bound.read(metadata.current_queue_bound, 7);

                                            /*Blocking reaction*/
                                            if(metadata.current_queue_bound > metadata.rank) {
                                                bit<32> cost = metadata.current_queue_bound - metadata.rank;

                                                /*Decrease the bound of all the following queues a factor equal to the cost of the blocking*/
                                                queue_bound.read(metadata.current_queue_bound, 0);
                                                queue_bound.write(0, (bit<32>)(metadata.current_queue_bound-cost));
                                                queue_bound.read(metadata.current_queue_bound, 1);
                                                queue_bound.write(1, (bit<32>)(metadata.current_queue_bound-cost));
                                                queue_bound.read(metadata.current_queue_bound, 2);
                                                queue_bound.write(2, (bit<32>)(metadata.current_queue_bound-cost));
                                                queue_bound.read(metadata.current_queue_bound, 3);
                                                queue_bound.write(3, (bit<32>)(metadata.current_queue_bound-cost));
                                                queue_bound.read(metadata.current_queue_bound, 4);
                                                queue_bound.write(4, (bit<32>)(metadata.current_queue_bound-cost));
                                                queue_bound.read(metadata.current_queue_bound, 5);
                                                queue_bound.write(5, (bit<32>)(metadata.current_queue_bound-cost));
                                                queue_bound.read(metadata.current_queue_bound, 6);
                                                queue_bound.write(6, (bit<32>)(metadata.current_queue_bound-cost));
                                                queue_bound.write(7, metadata.rank);
                                            } else {
                                                queue_bound.write(7, metadata.rank);
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
                // Print the queue bound and rank
                log_msg(" INFO C_Rank : {} Q_Bound : {} ", {metadata.rank, metadata.current_queue_bound});
                ipv4_lpm.apply();
                log_msg(" INFO Class : {} T_Latency : {} R_Latency : {} Priority : {} ", {hdr.int_header.class, hdr.int_header.t_latency, hdr.int_header.r_latency, hdr.int_header.priority});

            }
        }
    }
}
