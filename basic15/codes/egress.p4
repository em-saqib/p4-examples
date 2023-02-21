/*************************************************************************
****************  E G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

#include "queue.p4"

control MyEgress(inout headers hdr,
                 inout local_metadata_t metadata,
                 inout standard_metadata_t standard_metadata) {
    apply {

          // Store queueing data into metadata
          //metadata.queueing_metadata.enq_timestamp = standard_metadata.enq_timestamp;
          //metadata.queueing_metadata.enq_qdepth = standard_metadata.enq_qdepth;
          //metadata.queueing_metadata.deq_timedelta = standard_metadata.deq_timedelta;
          //metadata.queueing_metadata.deq_qdepth = standard_metadata.deq_qdepth;
          metadata.q_delay = (bit<13>)standard_metadata.deq_timedelta;

          //hdr.int_header.r_latency = hdr.int_header.r_latency - metadata.q_delay;
          //log_msg(" INFO Q_delay : {} R_latency : {} ", {metadata.q_delay, hdr.int_header.r_latency});


     }
}
