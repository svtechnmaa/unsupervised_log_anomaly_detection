# es_connection = {
#     "host": "10.98.100.109",
#     "port": 9200,
#     "user": "elastic",
#     "password": "juniper@123"
# }
ticket_db = {
    "host": "10.98.100.107",
    "port": 3306,
    "user": "juniper",
    "password": "juniper@123"
}
num_core = 4
pattern_dict = {'KB31709': 'LUCHIP.*Display trap-info logic not initialized',
'KB32155': 'Uninitialized Read Error',
'KB31743': 'LUCHIP\(\d*\) DDR\d VERIFY_RETRY_LIMIT of \d* exceeded',
'KB31715': 'LUCHIP.* IDMEM.*read error',
'KB31714': 'LUCHIP.*RD_NACK.*TOE Read',
'KB31713': 'Secondary PPE.*zone.*timeout',
'KB31708': 'SHARED LMEM errors require LUCHIP.*PPE.*disable',
'KB31740': 'TOE ERROR.*DETECTED IN PFE.*TOE LU Stats',
'KB32168': 'HOST LOOPBACK WEDGE DETECTED',
'KB32162': 'lmem data error',
'KB32163': 'lmem addr error',
'KB32143': 'Errors async xtxn error',
'KB32142': 'Errors sync xtxn error',
'KB31901': 'LUCHIP\(\d*\) .*RMC .* Uncorrectable ECC .* EDMEM',
'KB31732': 'RamBIST:.*LU-CHIP.* BIST: Memory Error',
'KB31731': 'LUCHIP.*RMC.*Correctable ECC .* cnt .* syn .* EDMEM',
'KB31727': 'LUCHIP.*pio_handle.*pio_read_u64.*failed',
'KB31728': 'LUCHIP.*HASH INT Status FPM Error',
'KB31726': 'LUCHIP.*PPE.*CBO.*mismatch.*rd.*exp',
'KB31716': 'LUCHIP.*PPE.*Errors lmem data error',
'KB31711': 'RMC.*Uninitialized EDMEM.*Read',
'KB31706': 'LUCHIP.* PPE_.* Errors KMB.* parity error',
'KB30724': 'LUCHIP\(\d*\).*RMC .* Uncorrectable ECC.*0x6db6db6d6db6db6d @ 0x.* EDMEM',
'KB20390': 'Errors ucode data error',
'KB31591': 'MQCHIP.*FI Error-cell sent to reorder engine',
'KB31583': 'MQCHIP.*FI Enqueuing error.*type.*seq.*stream',
'KB31582': 'MQCHIP.*DDRIF WO Checksum Error',
'KB31569': 'MQCHIP.*DDRIF FO.*Checksum Error',
'KB31689': 'MQCHIP.*WI parity error detected when read from ibuf',
'KB31688': 'MQCHIP.*CPQ RLDRAM single bit ECC error.*bank.*addr',
'KB31599': 'MQCHIP.*CPQ RLDRAM double bit ECC error.*bank.*addr',
'KB31593': 'MQCHIP.*MALLOC Pre-Q Reference Count underflow.*decrement below zero',
'KB31584': 'MQCHIP.*CPQ Sram parity error, errlog',
'KB31581': 'MQCHIP.*FO Request time-out error',
'KB31568': 'MQCHIP.*FI Cell underflow at the state stage',
'KB31739': 'MQCHIP.*PT CPT parity error detected',
'KB31592': 'MQCHIP.*OCM Fo.*Ddrif Parity Error',
'KB32161': 'Errors KM\w\[\d*\] parity error',
'KB32157': 'ucode sb data error',
'KB32156': 'gumem\[\d*\]\.par_protect',
'KB32158': 'Errors CBO\[\d*\]\ parity error',
'KB32353': 'XL.*cass_xr.*dbuf_protect Corrected XR DBUF',
'KB32154': 'Double-bit ECC error',
'KB32153': 'idmem_slice.*Corrected single bit ECC error',
'KB32152': '(PRB_EVENERR|PRB_ODDERR)',
'KB32144': '(SECONDARY_TIMEOUT|PRIMARY_TIMEOUT)',
'KB32137': 'filter\.pf0_1.alpha\[\d*\]\.protect',
'KB31684': 'XMCHIP.*MALLOC.*DMEM allocation memory parity error',
'KB32105': 'XMCHIP.*DDRIF:.*LLISTQ.*Parity error for free pointer SRAM',
'KB31697': 'XMCHIP.*OCM: .*parity error - Parity Error Address',
'KB31696': 'XMCHIP.*MALLOC.*DREF memory parity error',
'KB31680': 'XMCHIP.*WI.*Input pause buffer exceeded.*Check if the transmitter respects pause frames',
'KB32171': 'XMCHIP.*Cell packing interface error',
'KB32106': 'PRECL.*XM_engine.*instmem parity error detected',
'KB32005': 'XMCHIP.*CPQ1.*Queue un.*run indication',
'KB31737': 'XMCHIP.*WO.*Packet error - Error Packets',
'KB31736': 'XMCHIP.*PT.*Protect.*Log Error.*Log Address.*Multiple Errors',
'KB31735': 'XMCHIP.*LI.*Received a parcel with more than 512B accompanying data',
'KB31734': 'XMCHIP.*FI.*Link sanity checks.*Type',
'KB31733': 'XMCHIP.*LI.*Received a parcel from the HSL2 interface with EOPE',
'KB31703': 'XMCHIP.*PT.*Missing SOP.*EOP errors from input blocks',
'KB31702': 'XMCHIP.*FI.*Packet CRC error',
'KB31701': 'XMCHIP.*DRD.*WAN parcel timeout error',
'KB31698': 'XMCHIP.*PT.*Protect.*Parity error for CPFIFO data memory',
'KB31687': 'XMCHIP.*DDRIF.*Checksum error for FO/WO.*Channel.*Address.*Checksum Errors',
'KB31686': 'XMCHIP.*FI.*Aliasing on allocates error.*Pipe count',
'KB31685': 'XMCHIP.*EPM.*upon free pool',
'KB31682': 'XMCHIP.*FO.*Request timeout error.*Number of timeouts',
'KB31681': 'XMCHIP.*XXLCE.*Port Interrupts.*Ethernet Rx Stats Parity Error',
'KB31679': 'XMCHIP.*LI.*Received cookie size different from expected',
'KB31619': 'XMCHIP.*DRD.*Protect.*Parity error for DRD memory',
'KB31617': 'XMCHIP.*DRD.*Fabric parcel timeout error',
'KB31609': 'XMCHIP.*Scheduler:.*Protect:.*Parity error for tick table single port SRAM',
'KB31610': 'XMCHIP.*FI.*Protect.*Parity error for .* freepool SRAM',
'KB31608': 'XMCHIP.*WI CPQ Free Pointer SRAM Protect:.*Parity error',
'KB31607': 'XMCHIP.*MALLOC:.*SChunk allocation memory parity error',
'KB31601': 'XMCHIP.*Scheduler.*Protect.*Parity error for TDM table single port SRAM',
'KB31600': 'XMCHIP.*DRD0.*Reference count memory decrement error.*PCT',
'KB31611': 'XMCHIP.*FI.*Cell underflow at the state stage',
'KB31602': 'XMCHIP.*DRD.*Command sequence error',
'KB37469': 'XMCHIP_CMERROR_DDRIF_PROTECT_LLISTQ_SRAM_CHNK_CHKSUM \(0x70068\)',
'KB32890': 'XMCHIP.*HOSTIF: Protect: Parity error for SRAM in bank.*',
'KB33994': 'MQSS.*WANIO_CR.*Parity error detected for Tx SRAM - detected_txlink',
'KB32085': 'MQSS.*FO.*Parity error detected for output buffer control',
'KB31717': 'MQSS.*FO: Request timeout error - Number of timeouts .*, RC select .*, Stream',
'KB31718': 'MQSS.*LI.*Unroll TAIL length overflow',
'KB31722': 'EA.*HMCIF Rx.*Link.*Response FIFO .* overflow',
'KB31694': 'EA.*HMCIF Rx.*Link.*HMCIF Rx retry attempts failed',
'KB31693': 'EA.*HMCIF Rx.*Link.*HMC token overflow',
'KB32090': 'MQSS.*BCMF CBUF.*Parity error corrected for buffer free list memory for bank',
'KB32335': 'EA.*Checksum error detected on',
'KB32342': 'MQSS.*FI.*Child drop error',
'KB32333': 'MQSS.*LI.*Received a parcel with more than 512B accompanying data',
'KB32352': 'MQSS.*DRD.*CMD FSM state error',
'KB32343': 'MQSS.*FI.*Cell jump drop error',
'KB32334': 'MQSS.*Cell packing interface error',
'KB32291': 'EA.*HMCIO TX: AFIFO overflow event detected in Channel',
'KB32332': 'EA.*HMCIO RX: SFIFO overflow event detected in Channel',
'KB32119': 'HMM.*Lane.*TX RLL event',
'KB32087': 'EA.*Bist XRIF.*failed',
'KB32084': 'MQSS.*BCMW ICM.*Invalid cell sequence.*Packet start without SOP or 16K packet bytes without SOP',
'KB32088': 'MQSS.*FI.*Parity error detected for bank.*of CP table',
'KB32089': 'EA.*reports CM err HMC BIST has detected error',
'KB31720': 'MQSS.* FI: Cell underflow at the state stage \(Cell behind reorder window\) - Stream .* Count .*',
'KB31723': 'EA.*HMCIF.*HMCIF has no chunk index available for incoming WO read',
'KB31719': 'MQSS.*DRD.*Protect.*Parity error corrected for alloc state memory .* data32_log_err .* data32_log_address',
'KB31721': 'MQSS.*BCMF CBUF.*SRAM Protect.*Parity error detected for Bank.*Sub-Bank.*memory',
'KB31695': 'total number of corrected singlebit errors from HMC 1 exceeded threshold \d\d\d\d',
'KB31692': '.*CPQW Fast request is asserted for empty Queue',
'KB31691': 'CPQW Freelist Manager run out of avaliable fl pointers',
'KB31690': '.* Qdepth underrun error in Drop engine \d, ERR_LOG: Q_num: \d Dequeue byte count: \d',
'KB32344': '.* response packet with a FATAL state is received from HMC - State: 0x1f, Count \d',
'KB32091': '.*response packet with a FATAL state is received from HMC - State: 0x7f, Count \d',
'KB37050': '.*ECC single bit parity error',
'KB35999': 'PHY stream.*to drain',
'KB34996': 'exited on signal.*|.*clock failure',
'KB37507': 'ECC Protect: Parity error corrected for FlexMem slices',
'TSB74336':'(Machine check events loggedkernel.*Machine check events logged|CPU_CMERROR_DDR_CORRECTABLE_MINOR)',
'KB37331': 'TPCI PIO Read errors seen in last second',
'KB30474': 'CHASSISD_I2CS_READBACK_ERROR: Readback error from I2C slave for FPC',
'KB78259': 'FI: Cell underflow errors with reorder engine pointers stalled',
'KB78191': 'XQSS_CMERROR_CPQW_ERR_INT_FSET_LP_RD_ERR',
'KB72383': 'LUCHIP.*LKUP_ASIC_SINGLE_BIT_ECC',
'KB70778': 'MQSS.*: DRD.* Protect: Multiple Errors',
'KB77691': 'LKUP_ASIC_HSL2_MAJOR_CRC_ERROR',
'KB77156': 'MQSS_CMERROR_DRD_UNROLL_SRAM_PAR_PROTECT_FSET_REG_DETECTED_TO_CPQW_FIFO_LOW',
'KB77455': 'MQSS_CMERROR_MALLOC_SRAM_ECC_PROTECT_FSET_REG_CORRECTED_ALLOC_PFB_MEM0',
'KB76334': 'MQSS_CMERROR_FO_MEM_PAR_PROTECT_FSET_REG_DETECTED_OBUF_DATA',
'KB77470': 'MQSS_CMERROR_DRD_TOP_ECC2_PROTECT_FSET_REG_CORRECTED_FL_FIFO_MEM0',
'KB76675': 'EACHIP_CMERROR_HMCIF_RX_ECC1_PROTECT_FSET_REG_CORRECTED_FO_CHKSUM_IDX',
'KB72915': 'MQSS.* FI: Protect: Parity error detected for timer SRAM',
'KB75988': 'XMCHIP.*: XMCHIP.*: DRD.*: Command sequence error',
'KB75209': 'FI_PROTECT: .* Parity error for .* Freepool SRAM',
'KB75103': 'MQSS_CMERROR_CPQF_SRAM_PAR_PROTECT_FSET_REG_DETECTED_PFBE',
'KB70266': 'EACHIP_CMERROR_XIF_MQSS_PAR_PROTECT_FSET_REG_DETECTED_OCM'
}
data_path = "/var/tmp/for_unsupervised_report"
# MAX_SIZE_MB = 200
