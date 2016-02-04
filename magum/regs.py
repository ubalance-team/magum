"""This file contains all the registers used by fxos8700cq and fxas2100c"""
# -*- coding: utf-8 -*-

I2C_AM_ADDRESS		= 0x1e	# I2C accelerometer/magnetometer address
I2C_G_ADDRESS		= 0x20  # I2C gyroscope address

# ACCELEROMETER REGISTERS
# Device Configuration
A_STATUS			= 0x00	# Data ready status or FIFO status configuration regsiter
A_TRIG_CFG			= 0X0a	# FIFO trigger configuration register
A_SYSMOD			= 0x0b	# Current device operating mode register
A_INT_SOURCE		= 0x0c
A_WHO_AM_I			= 0x0d
A_CTRL_REG1			= 0x2a 	# standby/active,autowake,output_data_rate,lnoise,fast_read mode accelerometer register
A_CTRL_REG2			= 0x2b	# st_bit,rst_bit,Accelerometer Sleep mode,OSR mode selection,Auto-sleep mode,Accelerometer Wake mode OSR mode selection 
A_CTRL_REG3			= 0x2c	# Interrupt control register
A_CTRL_REG4			= 0x2d	# Interrupt enable register
A_CTRL_REG5			= 0x2e	# Interrupt routing configuration register

# Auto-Sleep trigger
A_ASPL_COUNT		= 0x29	# ASPL_COUNT register: sets the minimum time period of event flag inactivity required to initiate a change from the current active mode ODR value specified in CTRL_REG1[dr] to the Sleep mode ODR value specified in CTRL_REG1[aslp_rate], provided that CTRL_REG2[slpe] = 1					

# Temperature
A_TEMP 				= 0X51

# Accelerometer output data registers
A_OUT_X_MSB 		= 0x01 	# out_x_msb accelerometer register
A_OUT_X_LSB 		= 0x02 	# out_x_lsb accelerometer register
A_OUT_Y_MSB 		= 0x03 	# out_y_msb accelerometer register
A_OUT_Y_LSB 		= 0x04 	# out_y_lsb accelerometer register
A_OUT_Z_MSB 		= 0x05 	# out_z_msb accelerometer register
A_OUT_Z_LSB 		= 0x06 	# out_z_lsb accelerometer register

# Accelerometer FIFO
A_F_SETUP			= 0x09	# FIFO buffer operating mode, FIFO sample count watermark register configuration

# Accelerometer sensor data configuration
A_XYZ_DATA_CFG		= 0x0e  # accelerometer full scale range register

# Accelerometer High-Pass filter
A_HP_FILTER_CUTOFF	= 0x0f  # High-pass filter cutoff frequency settings register

# Portrait/Landscape detection
A_PL_STATUS			= 0x10
A_PL_CFG		    = 0x11	# Portrait/Landscape configuration register
A_PL_COUNT			= 0x12	# debounce count settings register
A_PL_BF_ZCOMP		= 0x13
A_PL_THS_REG		= 0x14

# Freefall motion detection
A_FFMT_CFG			= 0x15	# Freefall/motion configuration register
A_FFMT_SRC			= 0x16
A_FFMT_THS 			= 0x17
A_FFMT_THS_X_MSB	= 0x73
A_FFMT_THS_X_LSB	= 0x74
A_FFMT_THS_Y_MSB	= 0x75
A_FFMT_THS_Y_LSB	= 0x76
A_FFMT_THS_Z_MSB	= 0x77
A_FFMT_THS_Z_LSB	= 0x78
A_FFMT_COUNT		= 0x18

# Accelerometer vector-magnitude function
A_VECM_CFG			= 0x5f	# latch enable mode, set initial reference values, reference values updating mode, accelerometer vector-magnitude function enable/disable
A_VECM_THS_MSB		= 0x60
A_VECM_THS_LSB		= 0x61
A_VECM_CNT 			= 0x62
A_VECM_INITX_MSB	= 0x63
A_VECM_INITX_LSB	= 0x64
A_VECM_INITY_MSB	= 0x65
A_VECM_INITY_LSB	= 0x66
A_VECM_INITZ_MSB	= 0x67
A_VECM_INITZ_LSB	= 0x68


# Transient acceleration detection 
A_TRANSIENT_CFG		= 0x1d	# Transient event flag latch enable, Z-axis transient event flag enable, Y-axis transient event flag enable, X-axis transient event flag enable, Transient function high-pass filter bypass enable
A_TRANSIENT_SRC		= 0x1e
A_TRANSIENT_THS		= 0x1f
A_TRANSIENT_COUNT	= 0x20

# Pulse detection
A_PULSE_CFG			= 0x21	# pulse event detection function configuration register
A_PULSE_SRC			= 0x22
A_PULSE_THSX		= 0x23
A_PULSE_THSY		= 0x24
A_PULSE_THSZ		= 0x25
A_PULSE_TMLT		= 0x26
A_PULSE_LTCY		= 0x27
A_PULSE_WIND		= 0x28

# accelerometer offset correction
A_OFF_X				= 0x2f
A_OFF_Y				= 0x30
A_OFF_Z				= 0x31

# GYROSCOPE REGITERS
G_STATUS 			= 0x00 # easy reading of the relevant status register or the first sample stored in the FIFO
G_DR_STATUS			= 0x07 # sample data acquisition status, reflects the real-time updates to the OUT registers 
G_F_STATUS			= 0x08 # when FIFO is enabled, indicates the current status of the FIFO
G_F_SETUP			= 0x09 # FIFO configurations
G_F_EVENT			= 0x0A # used to monitor the FIFO event status
G_INT_SOURCE_FLAGS	= 0x0b # provides the event-flag status for the interrupt generating functions within the device
G_WHO_AM_I			= 0x0c # contains the device identifier which is factory programmed to 0xD7 
G_CTRL_REG0			= 0x0d # used for general control and configuration of the device
G_RT_CFG			= 0x0e # enables the Rate Threshold interrupt generation
G_RT_SRC			= 0x0f # indicates the source of the Rate Threshold event
G_RT_THS			= 0x10 #  sets the threshold limit for the detection of the rate and the debounce counter mode
G_RT_COUNT			= 0x11 # sets the number of debounce counts
G_TEMP 				= 0x12 # contains an 8-bit 2's complement temperature value with a range of –128 °C to +127 °C and a scaling of 1 °C/LSB
G_CTRL_REG1 		= 0x13 # configures the device ODR 
G_CTRL_REG2   		= 0x14 # enables and assigns the output pin(s) and logic polarities for the various interrupt sources
G_CTRL_REG3 		= 0x15 # enables FSR expansion, ext. power control input, options to modify the auto-increment read address pointer behavior when doing burst reads of the FIFO data
G_OUT_X_MSB 		= 0x01 # g_out_x_msb gyroscope register
G_OUT_X_LSB 		= 0x02 # g_out_x_lsb gyroscope register
G_OUT_Y_MSB 		= 0x03 # g_out_y_msb gyroscope register
G_OUT_Y_LSB 		= 0x04 # g_out_y_lsb gyroscope register
G_OUT_Z_MSB 		= 0x05 # g_out_z_msb gyroscope register
G_OUT_Z_LSB 		= 0x06 # g_out_z_lsb gyroscope register


# MAGNETOMETER REGISTERS
# Magnetometer data registers
M_DR_STATUS		 	= 0x32	# Magnetic data-ready status register
M_OUT_X_MSB		 	= 0x33
M_OUT_X_LSB 	 	= 0x34
M_OUT_Y_MSB 	 	= 0x35
M_OUT_Y_LSB 	 	= 0x36
M_OUT_Z_MSB 	 	= 0x37
M_OUT_Z_LSB 	 	= 0x38
M_CMP_X_MSB		 	= 0x39
M_CMP_X_LSB 	 	= 0x3a
M_CMP_Y_MSB		 	= 0x3b
M_CMP_Y_LSB		 	= 0x3c
M_CMP_Z_MSB		 	= 0x3d
M_CMP_Z_LSB		 	= 0x3e
M_MAX_X_MSB		 	= 0x45
M_MAX_X_LSB		 	= 0x46
M_MAX_Y_MSB		 	= 0x47
M_MAX_Y_LSB		 	= 0x48
M_MAX_Z_MSB		 	= 0x49
M_MAX_Z_LSB		 	= 0x4a
M_MIN_X_MSB		 	= 0x4b
M_MIN_X_LSB		 	= 0x4c
M_MIN_Y_MSB		 	= 0x4d
M_MIN_Y_LSB		 	= 0x4e
M_MIN_Z_MSB		 	= 0x4f
M_MIN_Z_LSB		 	= 0x50

# Magnetometer offset correction
M_OFF_X_MSB 	 	= 0x3f
M_OFF_X_LSB 	 	= 0x40
M_OFF_Y_MSB 	 	= 0x41
M_OFF_Y_LSB 	 	= 0x42
M_OFF_Z_MSB 	 	= 0x43
M_OFF_Z_LSB 	 	= 0x44

# Magnetometer threshold function
M_THS_CFG		 	= 0x52	# Magnetic-field threshold detection configuration register
M_THS_SRC		 	= 0x53
M_THS_X_MSB 	 	= 0x54
M_THS_X_LSB 	 	= 0x55
M_THS_Y_MSB 	 	= 0x56
M_THS_Y_LSB 	 	= 0x57
M_THS_Z_MSB 	 	= 0x58
M_THS_Z_LSB 	 	= 0x59
M_THS_COUNT 	 	= 0x5a

# Magnetometer control registers
M_CTRL_REG1 	 	= 0x5b	# Auto-Calibration, One-shot reset register
M_CTRL_REG2 	 	= 0x5c  # min/MAX detection config, sensor reset frequency register
M_CTRL_REG3 	 	= 0x5d	# measur. RAW mode, OSR in Auto-sleep, self-test configuration register
M_INT_SRC		 	= 0x5e

# Magnetometer vector-magnitude function
M_VECM_CFG		 	= 0x69	# vector-magnitude configuration register
M_VECM_THS_MSB	 	= 0x6a
M_VECM_THS_LSB	 	= 0x6b
M_VECM_CNT		 	= 0x6c
M_VECM_INITX_MSB 	= 0x6d
M_VECM_INITX_LSB 	= 0x6e
M_VECM_INITY_MSB 	= 0x6f
M_VECM_INITY_LSB 	= 0x70
M_VECM_INITZ_MSB 	= 0x71
M_VECM_INITZ_LSB 	= 0x72

COMPLETE_REGS_DICT	= {'A_TRIG_CFG':A_TRIG_CFG,'A_CTRL_REG1':A_CTRL_REG1,'A_CTRL_REG2':A_CTRL_REG2,'A_CTRL_REG3':A_CTRL_REG3,'A_CTRL_REG4':A_CTRL_REG4,'A_CTRL_REG5':A_CTRL_REG5,
                       'A_ASPL_COUNT':A_ASPL_COUNT,'A_F_SETUP':A_F_SETUP,'A_XYZ_DATA_CFG':A_XYZ_DATA_CFG,'A_HP_FILTER_CUTOFF':A_HP_FILTER_CUTOFF,'A_PL_CFG':A_PL_CFG,
			    	   'A_PL_COUNT':A_PL_COUNT,'A_PL_BF_ZCOMP':A_PL_BF_ZCOMP,'A_PL_THS_REG':A_PL_THS_REG,'A_FFMT_CFG':A_FFMT_CFG,'A_FFMT_THS':A_FFMT_THS,'A_FFMT_COUNT':A_FFMT_COUNT,
			    	   'A_VECM_CFG':A_VECM_CFG,'A_VECM_THS_MSB':A_VECM_THS_MSB,'A_TRANSIENT_CFG':A_TRANSIENT_CFG,
			           'A_TRANSIENT_THS':A_TRANSIENT_THS,'A_TRANSIENT_COUNT':A_TRANSIENT_COUNT,'A_PULSE_CFG':A_PULSE_CFG,'A_PULSE_TMLT':A_PULSE_TMLT,'A_PULSE_LTCY':A_PULSE_LTCY,
			           'A_OFF_X':A_OFF_X,'A_OFF_Y':A_OFF_Y,'A_OFF_Z':A_OFF_Z,'M_OFF_X_MSB':M_OFF_X_MSB,'M_OFF_X_LSB':M_OFF_X_LSB,'M_OFF_Y_MSB':M_OFF_Y_MSB,'M_OFF_Y_LSB':M_OFF_Y_LSB,
			           'M_OFF_Z_MSB':M_OFF_Z_MSB,'M_OFF_Z_LSB':M_OFF_Z_LSB,'M_THS_CFG':M_THS_CFG,'M_THS_COUNT':M_THS_COUNT,
			           'M_CTRL_REG1':M_CTRL_REG1,'M_CTRL_REG2':M_CTRL_REG2,'M_CTRL_REG3':M_CTRL_REG3,'M_VECM_CFG':M_VECM_CFG,
			           'M_VECM_THS_MSB':M_VECM_THS_MSB,'M_VECM_THS_LSB':M_VECM_THS_LSB,'M_VECM_CNT':M_VECM_CNT,'G_F_SETUP':G_F_SETUP,
			           'G_CTRL_REG0':G_CTRL_REG0,'G_RT_CFG':G_RT_CFG,'G_RT_THS':G_RT_THS,'G_RT_COUNT':G_RT_COUNT,
			           'G_CTRL_REG1':G_CTRL_REG1,'G_CTRL_REG2':G_CTRL_REG2,'G_CTRL_REG3':G_CTRL_REG3}

A_CREGS_LIST = ['A_TRIG_CFG','A_CTRL_REG1','A_CTRL_REG2','A_CTRL_REG3','A_CTRL_REG4','A_CTRL_REG5','A_ASPL_COUNT','A_F_SETUP','A_XYZ_DATA_CFG','A_HP_FILTER_CUTOFF','A_PL_CFG',
			    'A_PL_COUNT','A_PL_BF_ZCOMP','A_PL_THS_REG','A_FFMT_CFG','A_FFMT_THS','A_FFMT_COUNT','A_VECM_CFG','A_VECM_THS_MSB','A_TRANSIENT_CFG',
			    'A_TRANSIENT_THS','A_TRANSIENT_COUNT','A_PULSE_CFG','A_PULSE_TMLT','A_PULSE_LTCY','A_OFF_X','A_OFF_Y','A_OFF_Z']
M_CREG_LIST =  ['M_OFF_X_MSB','M_OFF_X_LSB','M_OFF_Y_MSB','M_OFF_Y_LSB','M_OFF_Z_MSB','M_OFF_Z_LSB','M_THS_CFG','M_THS_COUNT',
			    'M_CTRL_REG1','M_CTRL_REG2','M_CTRL_REG3','M_VECM_CFG','M_VECM_THS_MSB','M_VECM_THS_LSB','M_VECM_CNT']
G_CREG_LIST =  ['G_F_SETUP','G_CTRL_REG0','G_RT_CFG','G_RT_THS','G_RT_COUNT','G_CTRL_REG1','G_CTRL_REG2','G_CTRL_REG3']