#-------------------------------------------------------------------------------
# Name:        asm2bin
# Purpose:     Assembler 2 Binary Translator
#
# Author:      Sehktel
#
# Created:     30.01.2025
# Copyright:   (c) Sehktel 2025
# Licence:     MIT
#-------------------------------------------------------------------------------
import binascii

DEBUG = True

dict_clear = {
    'NOP'   : [0x00, 1],
    'RR'    : [0x03, 1],
    'RRC'   : [0x13, 1],
    'RET'   : [0x22, 1],
    'RL'    : [0x23, 1],
    'RETI'  : [0x32, 1],
    'RLC'   : [0x33, 1],
    'JMP'   : [0x73, 1],
    'DIV'   : [0x84, 1],
    'MUL'   : [0xA4, 1],
    'reserved':[0xA5,1],
    'SWAP'  : [0xC4, 1],
    'DA'    : [0xD4, 1],
    'JC'    : [0x40, 1],
    'JNC'   : [0x50, 1],
    'JZ'    : [0x60, 1],
    'JNZ'   : [0x70, 1],
    'SJMP'  : [0x80, 1],
    'PUSH'  : [0xC0, 1],
    'POP'   : [0xD0, 1],
    'LJMP'  : [0x02, 1],
    'LCALL' : [0x12, 1],
    'JBC'   : [0x10, 1],
    'JB'    : [0x20, 1],
    'JNB'   : [0x30, 1]

}

clear  = ['NOP',  'RR',    'RRC', 'RET',      'RL',   'RETI', 'RLC',
          'JMP',  'DIV',   'MUL', 'reserved', 'SWAP', 'DA',   'JC',
          'JNC',  'JZ',    'JNZ', 'SJMP',     'PUSH', 'POP',
          'LJMP', 'LCALL', 'JBC', 'JB',       'JNB']

light  = ['MOVC', 'SETB', 'XCHD',  'CPL',  'CLR' ]

middle = ['MOVX', 'AJMP', 'ACALL', 'DJNZ', 'XCH', 'DEC', 'ADD',
          'ADDC', 'SUBB', 'CJNE',  'INC',  'XRL', 'ORL', 'ANL']

hard   = ['MOV']


def op_clear(line):
##    1    NOP
##    1    RR
##    1    RRC
##    1    RET
##    1    RL
##    1    RETI
##    1    RLC
##    1    JMP
##    1    DIV
##    1    MUL
##    1    reserved
##    1    SWAP
##    1    DA
##    1    JC
##    1    JNC
##    1    JZ
##    1    JNZ
##    1    SJMP
##    1    PUSH
##    1    POP
##    1    LJMP
##    1    LCALL
##    1    JBC
##    1    JB
##    1    JNB

    linesplie = line.strip().split()
    op = linesplie[0]
    arg1 = ''
    arg2 = ''
    if len(linesplie) > 1:
        arg1 = linesplie[1]
    if len(linesplie) > 2:
        arg2 = linesplie[2]

    ophex = dict_clear[op][0]

    print(f'{ophex:02X} ', end='')

    if arg1.startswith('0x'):
        arg1 = binascii.unhexlify(arg1[2:-1]) if arg1[-1] == ',' else binascii.unhexlify(arg1[2:])
        for b in arg1:
            print(f'{b:02X} ',  end='')

    if arg2.startswith('0x'):
        print(f'{arg2[2:4]} ', end='')

    print('  : ', line) if DEBUG else print()


def op_light(line):
##    2    MOVC
##    2    SETB
##    2    XCHD
##    3    CPL
##    3    CLR
    linesplie = line.strip().split()
    op   = linesplie[0]
    arg1 = linesplie[1]
    arg2 = linesplie[2] if len(linesplie) > 2 else ''

    match op:
        case 'MOVC':
            match arg2:
                case '@A+PC':
                    print('0x83')
            match arg2:
                case '@A+DPTR':
                    print('0x93')

        case 'SETB':
            match arg1:
                case 'C':
                    print('0xD3')
                case _:
                    print('0xD2', arg1) #f'{arg1:02X}')

        case 'XCHD':
            match arg2:
                case '@R0':
                    print('02D6')
            match arg2:
                case '@R1':
                    print('0xD7')

        case 'CPL':
            match arg1:
                case 'A':
                    print('0xF4')
                case 'C':
                    print('0xB3')
                case _:
                    print('0xB2', arg1) #f'{arg1:02X}')

        case 'CLR':
            match arg1:
                case 'A':
                    print('0xE4')
                case 'C':
                    print('0xC3')
                case _:
                    print('0xC2', arg1) #f'{arg1:02X}')

    print('  : ', line) if DEBUG else print()


def op_middle(line):
##    6    MOVX
##    8    AJMP
##    8    ACALL
##    9    DJNZ
##    11    XCH
##    12    DEC
##    12    ADD
##    12    ADDC
##    12    SUBBx
##    12    CJNE
##    13    INC
##    14    XRL
##    16    ORL
##    16    ANL
    linesplie = line.strip().split()
    op   = linesplie[0]
    arg1 = linesplie[1]
    arg2 = linesplie[2] if len(linesplie) > 2 else ''
    arg3 = linesplie[3] if len(linesplie) > 3 else ''

    match op:
        case 'MOVX':
##    0xE0    1    MOVX A,@DPTR
##    0xE2    1    MOVX A,@R0
##    0xE3    1    MOVX A,@R1
##    0xF0    1    MOVX @DPTR,A
##    0xF2    1    MOVX @R0,A
##    0xF3    1    MOVX @R1,A
            arg1 = arg1.replace(',','')
            match arg1:
                case 'A':
                    match arg2:
                        case '@DPTR':
                            print('0xE0')
                        case '@R0':
                            print('0xE2')
                        case '@R1':
                            print('0xE3')
            match arg2:
                case 'A':
                    match arg1:
                        case '@DPTR':
                            print('0xF0')
                        case '@R0':
                            print('0xF2')
                        case '@R1':
                            print('0xF3')

        case 'AJMP':
            addrh = (int(arg1[2:4], 16)) & 0x07
            addrl = (int(arg1[4:6], 16)) & 0xFF
            cmmnd = 0x01
            code = ((( addrh << 5 ) | cmmnd) << 8 ) | addrl

        case 'ACALL':
            addrh = (int(arg1[2:4], 16)) & 0x07
            addrl = (int(arg1[4:6], 16)) & 0xFF
            cmmnd = 0x11
            code = ((( addrh << 5 ) | cmmnd) << 8 ) | addrl
            print(f'{code:04X}')

        case 'DJNZ':
##    0xD8    2    DJNZ R0    1    0
##    0xD9    2    DJNZ R1    1    0
##    0xDA    2    DJNZ R2    1    0
##    0xDB    2    DJNZ R3    1    0
##    0xDC    2    DJNZ R4    1    0
##    0xDD    2    DJNZ R5    1    0
##    0xDE    2    DJNZ R6    1    0
##    0xDF    2    DJNZ R7    1    0
##    0xD5    3    DJNZ       1    1
            match arg1:
                case 'R0':
                    print('0xD8', arg2)
                case 'R1':
                    print('0xD8', arg2)
                case 'R2':
                    print('0xD8', arg2)
                case 'R3':
                    print('0xD8', arg2)
                case 'R4':
                    print('0xD8', arg2)
                case 'R5':
                    print('0xD8', arg2)
                case 'R6':
                    print('0xD8', arg2)
                case 'R7':
                    print('0xD8', arg2)
                case _:
                    print('0xD5', arg1, arg2)
        case 'XCH':
            match arg2:
##    0xC6    1    XCH A,@R0    0    0
##    0xC7    1    XCH A,@R1    0    0
##    0xC8    1    XCH A,R0     0    0
##    0xC9    1    XCH A,R1     0    0
##    0xCA    1    XCH A,R2     0    0
##    0xCB    1    XCH A,R3     0    0
##    0xCC    1    XCH A,R4     0    0
##    0xCD    1    XCH A,R5     0    0
##    0xCE    1    XCH A,R6     0    0
##    0xCF    1    XCH A,R7     0    0
##    0xC5    2    XCH A        1    0
                case '@R0':
                    print('0xC6')
                case '@R1':
                    print('0xC7')
                case 'R0':
                    print('0xC8')
                case 'R1':
                    print('0xC9')
                case 'R2':
                    print('0xCA')
                case 'R3':
                    print('0xCB')
                case 'R4':
                    print('0xCC')
                case 'R5':
                    print('0xCD')
                case 'R6':
                    print('0xCE')
                case 'R7':
                    print('0xCF')
                case _:
                    print('0xC5', arg2)

        case 'DEC':
##    0x14    1    DEC A      0    0
##    0x16    1    DEC @R0    0    0
##    0x17    1    DEC @R1    0    0
##    0x18    1    DEC R0     0    0
##    0x19    1    DEC R1     0    0
##    0x1A    1    DEC R2     0    0
##    0x1B    1    DEC R3     0    0
##    0x1C    1    DEC R4     0    0
##    0x1D    1    DEC R5     0    0
##    0x1E    1    DEC R6     0    0
##    0x1F    1    DEC R7     0    0
##    0x15    2    DEC        1    0
            match arg1:
                case 'A':
                    print('0x14')
                case '@R0':
                    print('0x16')
                case '@R1':
                    print('0x17')
                case 'R0':
                    print('0x18')
                case 'R1':
                    print('0x19')
                case 'R2':
                    print('0x1A')
                case 'R3':
                    print('0x1B')
                case 'R4':
                    print('0x1C')
                case 'R5':
                    print('0x1D')
                case 'R6':
                    print('0x1E')
                case 'R7':
                    print('0x1F')
                case _:
                    print('0x15', arg1)

        case 'ADD':
##    0x26    1    ADD A,@R0    0    0    ''
##    0x27    1    ADD A,@R1    0    0    ''
##    0x28    1    ADD A,R0     0    0    ''
##    0x29    1    ADD A,R1     0    0    ''
##    0x2A    1    ADD A,R2     0    0    ''
##    0x2B    1    ADD A,R3     0    0    ''
##    0x2C    1    ADD A,R4     0    0    ''
##    0x2D    1    ADD A,R5     0    0    ''
##    0x2E    1    ADD A,R6     0    0    ''
##    0x2F    1    ADD A,R7     0    0    ''
##    0x24    2    ADD A        1    0    '#'
##    0x25    2    ADD A        1    0    ''
            match arg2:
                case '@R0':
                    print('0x26')
                case '@R1':
                    print('0x27')
                case 'R0':
                    print('0x28')
                case 'R1':
                    print('0x29')
                case 'R2':
                    print('0x2A')
                case 'R3':
                    print('0x2B')
                case 'R4':
                    print('0x2C')
                case 'R5':
                    print('0x2D')
                case 'R6':
                    print('0x2E')
                case 'R7':
                    print('0x2F')
                case _:
                    if arg2.startswith('#'):
                        print('0x24', arg2[1:]) # skip # in #0x24 arg
                    else:
                        print('0x25', arg2)

            pass
        case 'ADDC':
##    0x36    1    ADDC A,@R0    0    0    ''
##    0x37    1    ADDC A,@R1    0    0    ''
##    0x38    1    ADDC A,R0     0    0    ''
##    0x39    1    ADDC A,R1     0    0    ''
##    0x3A    1    ADDC A,R2     0    0    ''
##    0x3B    1    ADDC A,R3     0    0    ''
##    0x3C    1    ADDC A,R4     0    0    ''
##    0x3D    1    ADDC A,R5     0    0    ''
##    0x3E    1    ADDC A,R6     0    0    ''
##    0x3F    1    ADDC A,R7     0    0    ''
##    0x34    2    ADDC A        1    0    '#'
##    0x35    2    ADDC A        1    0    ''
            match arg2:
                case '@R0':
                    print('0x36')
                case '@R1':
                    print('0x37')
                case 'R0':
                    print('0x38')
                case 'R1':
                    print('0x39')
                case 'R2':
                    print('0x3A')
                case 'R3':
                    print('0x3B')
                case 'R4':
                    print('0x3C')
                case 'R5':
                    print('0x3D')
                case 'R6':
                    print('0x3E')
                case 'R7':
                    print('0x3F')
                case _:
                    if arg2.startswith('#'):
                        print('0x34', arg2[1:]) # skip # in #0x34 arg
                    else:
                        print('0x35', arg2)
        case 'SUBB':
##    0x96    1    SUBB A,@R0    0    0    ''
##    0x97    1    SUBB A,@R1    0    0    ''
##    0x98    1    SUBB A,R0     0    0    ''
##    0x99    1    SUBB A,R1     0    0    ''
##    0x9A    1    SUBB A,R2     0    0    ''
##    0x9B    1    SUBB A,R3     0    0    ''
##    0x9C    1    SUBB A,R4     0    0    ''
##    0x9D    1    SUBB A,R5     0    0    ''
##    0x9E    1    SUBB A,R6     0    0    ''
##    0x9F    1    SUBB A,R7     0    0    ''
##    0x94    2    SUBB A        1    0    '#'
##    0x95    2    SUBB A        1    0    ''
            match arg2:
                case '@R0':
                    print('0x96')
                case '@R1':
                    print('0x97')
                case 'R0':
                    print('0x98')
                case 'R1':
                    print('0x99')
                case 'R2':
                    print('0x9A')
                case 'R3':
                    print('0x9B')
                case 'R4':
                    print('0x9C')
                case 'R5':
                    print('0x9D')
                case 'R6':
                    print('0x9E')
                case 'R7':
                    print('0x9F')
                case _:
                    if arg2.startswith('#'):
                        print('0x94', arg2[1:]) # skip # in #0x34 arg
                    else:
                        print('0x95', arg2)

        case 'CJNE':
##    0xB4    3    CJNE A       1    1    '$'
##    0xB5    3    CJNE A       1    1    ''
##    0xB6    3    CJNE @R0     1    1    '$'
##    0xB7    3    CJNE @R1     1    1    '$'
##    0xB8    3    CJNE R0      1    1    '$'
##    0xB9    3    CJNE R1      1    1    '$'
##    0xBA    3    CJNE R2      1    1    '$'
##    0xBB    3    CJNE R3      1    1    '$'
##    0xBC    3    CJNE R4      1    1    '$'
##    0xBD    3    CJNE R5      1    1    '$'
##    0xBE    3    CJNE R6      1    1    '$'
##    0xBF    3    CJNE R7      1    1    '$'
            arg1 = arg1.replace(',','')
            match arg1:
                case 'A':
                    if arg2.startswith('#'):
                        print('0xB4', arg2[1:], arg3) #  #0xB4 --> 0xB4
                    else:
                        print('0xB5', arg2, arg3)
                case '@R0':
                    print('0xB6', arg2[1:], arg3)
                case '@R1':
                    print('0xB7', arg2[1:], arg3)
                case 'R0':
                    print('0xB8', arg2[1:], arg3)
                case 'R1':
                    print('0xB9', arg2[1:], arg3)
                case 'R2':
                    print('0xBA', arg2[1:], arg3)
                case 'R3':
                    print('0xBB', arg2[1:], arg3)
                case 'R4':
                    print('0xBC', arg2[1:], arg3)
                case 'R5':
                    print('0xBD', arg2[1:], arg3)
                case 'R6':
                    print('0xBE', arg2[1:], arg3)
                case 'R7':
                    print('0xBF', arg2[1:], arg3)


        case 'INC':
##    0x04    1    INC A       0    0    ''
##    0x06    1    INC @R0     0    0    ''
##    0x07    1    INC @R1     0    0    ''
##    0x08    1    INC R0      0    0    ''
##    0x09    1    INC R1      0    0    ''
##    0x0A    1    INC R2      0    0    ''
##    0x0B    1    INC R3      0    0    ''
##    0x0C    1    INC R4      0    0    ''
##    0x0D    1    INC R5      0    0    ''
##    0x0E    1    INC R6      0    0    ''
##    0x0F    1    INC R7      0    0    ''
##    0xA3    1    INC DPTR    0    0    ''
##    0x05    2    INC         1    0    ''
            match arg1:
                case 'A':
                    print('0x04')
                case '@R0':
                    print('0x06')
                case '@R1':
                    print('0x07')
                case 'R0':
                    print('0x08')
                case 'R1':
                    print('0x09')
                case 'R2':
                    print('0x0A')
                case 'R3':
                    print('0x0B')
                case 'R4':
                    print('0x0C')
                case 'R5':
                    print('0x0D')
                case 'R6':
                    print('0x0E')
                case 'R7':
                    print('0x0F')
                case 'DPTR':
                    print('0xA3')
                case _:
                    print('0x05', arg1)

        case 'XRL':
##    0x62    2    XRL          1    0    'A'
##    0x63    3    XRL          1    1    '#'
##    0x64    2    XRL A        1    0    '#'
##    0x65    2    XRL A        1    0    ''
##    0x66    1    XRL A,@R0    0    0    ''
##    0x67    1    XRL A,@R1    0    0    ''
##    0x68    1    XRL A,R0     0    0    ''
##    0x69    1    XRL A,R1     0    0    ''
##    0x6A    1    XRL A,R2     0    0    ''
##    0x6B    1    XRL A,R3     0    0    ''
##    0x6C    1    XRL A,R4     0    0    ''
##    0x6D    1    XRL A,R5     0    0    ''
##    0x6E    1    XRL A,R6     0    0    ''
##    0x6F    1    XRL A,R7     0    0    ''
            arg1 = arg1.replace(',','')
            match arg1:
                case 'A':
                    match arg2:
                        case '@R0':
                            print('0x66')
                        case '@R1':
                            print('0x67')
                        case 'R0':
                            print('0x68')
                        case 'R1':
                            print('0x69')
                        case 'R2':
                            print('0x6A')
                        case 'R3':
                            print('0x6B')
                        case 'R4':
                            print('0x6C')
                        case 'R5':
                            print('0x6D')
                        case 'R6':
                            print('0x6E')
                        case 'R7':
                            print('0x6F')
                        case _:
                            if arg2.startswith('#'):
                                print('0x64', arg2[1:])#  #0x64 --> 0x64
                            else:
                                print('0x65', arg2)
                case _:
##    0x62    2    XRL          1    0    'A'
##    0x63    3    XRL          1    1    '#'
                    if arg2 == 'A':
                        print('0x62', arg1)
                    else:
                        print('0x63', arg1[1:]) #   #0x63 --> 0x63

        case 'ORL':
##    0x42    2    ORL          1    0    'A'
##    0x43    3    ORL          1    1    '#'
##    0x44    2    ORL A        1    0    '#'
##    0x45    2    ORL A        1    0    ''
##    0x46    1    ORL A,@R0    0    0    ''
##    0x47    1    ORL A,@R1    0    0    ''
##    0x48    1    ORL A,R0     0    0    ''
##    0x49    1    ORL A,R1     0    0    ''
##    0x4A    1    ORL A,R2     0    0    ''
##    0x4B    1    ORL A,R3     0    0    ''
##    0x4C    1    ORL A,R4     0    0    ''
##    0x4D    1    ORL A,R5     0    0    ''
##    0x4E    1    ORL A,R6     0    0    ''
##    0x4F    1    ORL A,R7     0    0    ''

##    0x72    2    ORL C        1    0    ''
##    0xA0    2    ORL C        1    0    '/'

            print(linesplie, ' :  ', end='')
            arg1 = arg1.replace(',','')
            match arg1:
                case 'A':
                    match arg2:
                        case '@R0':
                            print('0x46')
                        case '@R1':
                            print('0x47')
                        case 'R0':
                            print('0x48')
                        case 'R1':
                            print('0x49')
                        case 'R2':
                            print('0x4A')
                        case 'R3':
                            print('0x4B')
                        case 'R4':
                            print('0x4C')
                        case 'R5':
                            print('0x4D')
                        case 'R6':
                            print('0x4E')
                        case 'R7':
                            print('0x4F')
                        case _:
                            if arg2.startswith('#'):
                                print('0x44', arg2[1:])#  #0x44 --> 0x44
                            else:
                                print('0x45', arg2)
                case 'C':
##    0x72    2    ORL C        1    0    ''
##    0xA0    2    ORL C        1    0    '/'
                    if arg2.startswith('/'):
                        print('0xA0', arg2[1:]) #  /0xA0 --> 0xA0
                    else:
                        print('0x72', arg2)

                case _:
##    0x42    2    ORL          1    0    'A'
##    0x43    3    ORL          1    1    '#'
                    if arg2 == 'A':
                        print('0x42', arg1)
                    else:
                        print('0x43', arg1, arg2[1:]) #   #0x43 --> 0x43


        case 'ANL':
##    0x52    2    ANL          1    0    'A'
##    0x53    3    ANL          1    1    '#'
##    0x54    2    ANL A        1    0    '#'
##    0x55    2    ANL A        1    0    ''
##    0x56    1    ANL A,@R0    0    0    ''
##    0x57    1    ANL A,@R1    0    0    ''
##    0x58    1    ANL A,R0     0    0    ''
##    0x59    1    ANL A,R1     0    0    ''
##    0x5A    1    ANL A,R2     0    0    ''
##    0x5B    1    ANL A,R3     0    0    ''
##    0x5C    1    ANL A,R4     0    0    ''
##    0x5D    1    ANL A,R5     0    0    ''
##    0x5E    1    ANL A,R6     0    0    ''
##    0x5F    1    ANL A,R7     0    0    ''
##    0x82    2    ANL C        1    0    ''
##    0xB0    2    ANL C        1    0    '/'
            arg1 = arg1.replace(',','')
            match arg1:
                case 'A':
                    match arg2:
                        case '@R0':
                            print('0x56')
                        case '@R1':
                            print('0x57')
                        case 'R0':
                            print('0x58')
                        case 'R1':
                            print('0x59')
                        case 'R2':
                            print('0x5A')
                        case 'R3':
                            print('0x5B')
                        case 'R4':
                            print('0x5C')
                        case 'R5':
                            print('0x5D')
                        case 'R6':
                            print('0x5E')
                        case 'R7':
                            print('0x5F')
                        case _:
                            if arg2.startswith('#'):
                                print('0x54', arg2[1:]) # #0x54 --> 0x54
                            else:
                                print('0x55', arg2)

                case 'C':
##    0x82    2    ANL C        1    0    ''
##    0xB0    2    ANL C        1    0    '/'
                    if arg2.startswith('/'):
                        print('0xB0', arg2[1:]) # /0xB0 --> 0xB0
                    else:
                        print('0x82', arg2)
                case _:
##    0x52    2    ANL          1    0    'A'
##    0x53    3    ANL          1    1    '#'
                    if arg2 == 'A':
                        print('0x52')
                    else:
                        print('0x53', arg1, arg2[1:]) #  #0x53 --> 0x53


def op_hard(line):
##    0xE6    1    MOV A,@R0    0    0    ''
##    0xE7    1    MOV A,@R1    0    0    ''
##    0xE8    1    MOV A,R0     0    0    ''
##    0xE9    1    MOV A,R1     0    0    ''
##    0xEA    1    MOV A,R2     0    0    ''
##    0xEB    1    MOV A,R3     0    0    ''
##    0xEC    1    MOV A,R4     0    0    ''
##    0xED    1    MOV A,R5     0    0    ''
##    0xEE    1    MOV A,R6     0    0    ''
##    0xEF    1    MOV A,R7     0    0    ''

##    0xF6    1    MOV @R0,A    0    0    ''
##    0xF7    1    MOV @R1,A    0    0    ''
##    0xF8    1    MOV R0,A     0    0    ''
##    0xF9    1    MOV R1,A     0    0    ''
##    0xFA    1    MOV R2,A     0    0    ''
##    0xFB    1    MOV R3,A     0    0    ''
##    0xFC    1    MOV R4,A     0    0    ''
##    0xFD    1    MOV R5,A     0    0    ''
##    0xFE    1    MOV R6,A     0    0    ''
##    0xFF    1    MOV R7,A     0    0    ''

##    0x74    2    MOV A        1    0    '#'
##    0x76    2    MOV @R0      1    0    '#'
##    0x77    2    MOV @R1      1    0    '#'
##    0x78    2    MOV R0       1    0    '#'
##    0x79    2    MOV R1       1    0    '#'
##    0x7A    2    MOV R2       1    0    '#'
##    0x7B    2    MOV R3       1    0    '#'
##    0x7C    2    MOV R4       1    0    '#'
##    0x7D    2    MOV R5       1    0    '#'
##    0x7E    2    MOV R6       1    0    '#'
##    0x7F    2    MOV R7       1    0    '#'

##    0x86    2    MOV    1    0    '@R0'
##    0x87    2    MOV    1    0    '@R1'
##    0x88    2    MOV    1    0    'R0'
##    0x89    2    MOV    1    0    'R1'
##    0x8A    2    MOV    1    0    'R2'
##    0x8B    2    MOV    1    0    'R3'
##    0x8C    2    MOV    1    0    'R4'
##    0x8D    2    MOV    1    0    'R5'
##    0x8E    2    MOV    1    0    'R6'
##    0x8F    2    MOV    1    0    'R7'

##    0xA2    2    MOV C        1    0    ''
##    0xA6    2    MOV @R0      1    0    ''
##    0xA7    2    MOV @R1      1    0    ''
##    0xA8    2    MOV R0       1    0    ''
##    0xA9    2    MOV R1       1    0    ''
##    0xAA    2    MOV R2       1    0    ''
##    0xAB    2    MOV R3       1    0    ''
##    0xAC    2    MOV R4       1    0    ''
##    0xAD    2    MOV R5       1    0    ''
##    0xAE    2    MOV R6       1    0    ''
##    0xAF    2    MOV R7       1    0    ''
##    0xE5    2    MOV A        1    0    ''
##    0xF5    2    MOV ,A       1    0    'A'

##    0x90    3    MOV DPTR     2    0    '#'
##    0x75    3    MOV          1    1    '#'
##    0x92    2    MOV C        1    0    ''

    linesplie = line.strip().split()

    if DEBUG:
        print(linesplie, '  :  ', end='')

    op   = linesplie[0]
    arg1 = linesplie[1].replace(',','')
    arg2 = linesplie[2].replace(',','') if len(linesplie) > 2 else ''
    arg3 = linesplie[3].replace(',','') if len(linesplie) > 3 else ''

    match arg1:
##    0xE5    2    MOV A        1    0    ''
##    0x74    2    MOV A        1    0    '#'

##    0xE6    1    MOV A,@R0    0    0    ''
##    0xE7    1    MOV A,@R1    0    0    ''
##    0xE8    1    MOV A,R0     0    0    ''
##    0xE9    1    MOV A,R1     0    0    ''
##    0xEA    1    MOV A,R2     0    0    ''
##    0xEB    1    MOV A,R3     0    0    ''
##    0xEC    1    MOV A,R4     0    0    ''
##    0xED    1    MOV A,R5     0    0    ''
##    0xEE    1    MOV A,R6     0    0    ''
##    0xEF    1    MOV A,R7     0    0    ''
        case 'A':
            match arg2:
                case '@R0':
                    print('0xE6')
                case '@R1':
                    print('0xE7')
                case 'R0':
                    print('0xE8')
                case 'R1':
                    print('0xE9')
                case 'R2':
                    print('0xEA')
                case 'R3':
                    print('0xEB')
                case 'R4':
                    print('0xEC')
                case 'R5':
                    print('0xED')
                case 'R6':
                    print('0xEE')
                case 'R7':
                    print('0xEF')
                case _:
                    if arg2.startswith('#'):
                        print('0x74', arg2[1:]) #  #0x72 --> 0x72 'MOV A,#data'
                    else:
                        print('0xE5', arg2) # 'MOV A,data addr'
##    0x76    2    MOV @R0      1    0    '#'
##    0xF6    1    MOV @R0,A    0    0    ''
##    0xA6    2    MOV @R0      1    0    ''

##    0x77    2    MOV @R1      1    0    '#'
##    0xF7    1    MOV @R1,A    0    0    ''
##    0xA7    2    MOV @R1      1    0    ''

        case '@R0':
            match arg2[0]:
                case '#':
                    print('0x76', arg2[1:])
                case 'A':
                    print('0xF6')
                case _:
                    print('0xA6', arg2)
        case '@R1':
            match arg2[0]:
                case '#':
                    print('0x77', arg2[1:])
                case 'A':
                    print('0xF7')
                case _:
                    print('0xA7', arg2)

##    0x78    2    MOV R0       1    0    '#'
##    0xF8    1    MOV R0,A     0    0    ''
##    0xA8    2    MOV R0       1    0    ''

##    0x79    2    MOV R1       1    0    '#'
##    0xF9    1    MOV R1,A     0    0    ''
##    0xA9    2    MOV R1       1    0    ''
        case 'R0':
            match arg2[0]:
                case '#':
                    print('0x78', arg2[1:])
                case 'A':
                    print('0xF8')
                case _:
                    print('0xA8', arg2)
        case 'R1':
            match arg2[0]:
                case '#':
                    print('0x79', arg2[1:])
                case 'A':
                    print('0xF9')
                case _:
                    print('0xA9', arg2)
##    0x7A    2    MOV R2       1    0    '#'
##    0xFA    1    MOV R2,A     0    0    ''
##    0xAA    2    MOV R2       1    0    ''

##    0x7B    2    MOV R3       1    0    '#'
##    0xFB    1    MOV R3,A     0    0    ''
##    0xAB    2    MOV R3       1    0    ''
        case 'R2':
            match arg2[0]:
                case '#':
                    print('0x7A', arg2[1:])
                case 'A':
                    print('0xFA')
                case _:
                    print('0xAA', arg2)
        case 'R3':
            match arg2[0]:
                case '#':
                    print('0x7B', arg2[1:])
                case 'A':
                    print('0xFB')
                case _:
                    print('0xAB', arg2)

##    0x7C    2    MOV R4       1    0    '#'
##    0xFC    1    MOV R4,A     0    0    ''
##    0xAC    2    MOV R4       1    0    ''

##    0x7D    2    MOV R5       1    0    '#'
##    0xFD    1    MOV R5,A     0    0    ''
##    0xAD    2    MOV R5       1    0    ''

        case 'R4':
            match arg2[0]:
                case '#':
                    print('0x7C', arg2[1:])
                case 'A':
                    print('0xFC')
                case _:
                    print('0xAC', arg2)
        case 'R5':
            match arg2[0]:
                case '#':
                    print('0x7D', arg2[1:])
                case 'A':
                    print('0xFD')
                case _:
                    print('0xAD', arg2)

##    0x7E    2    MOV R6       1    0    '#'
##    0xFE    1    MOV R6,A     0    0    ''
##    0xAE    2    MOV R6       1    0    ''

##    0x7F    2    MOV R7       1    0    '#'
##    0xFF    1    MOV R7,A     0    0    ''
##    0xAF    2    MOV R7       1    0    ''

        case 'R6':
            match arg2[0]:
                case '#':
                    print('0x7E', arg2[1:])
                case 'A':
                    print('0xFE')
                case _:
                    print('0xAE', arg2)
        case 'R7':
            match arg2[0]:
                case '#':
                    print('0x7F', arg2[1:])
                case 'A':
                    print('0xFF')
                case _:
                    print('0xAF', arg2)

##    0x90    3    MOV DPTR     2    0    '#'
##    0x75    3    MOV          1    1    '#'
##    0xF5    2    MOV ,A       1    0    'A'
##    0xA2    2    MOV C        1    0    ''
        case 'DPTR':
            print('0x90', arg2[1:])#  #0x9090 --> 0x9090
        case 'C':
            print('0xA2', arg2)
        case _:
            match arg2:
                case 'A':
                    print('0xF5', arg1)

##    0x86    2    MOV    1    0    '@R0'
##    0x87    2    MOV    1    0    '@R1'
##    0x88    2    MOV    1    0    'R0'
##    0x89    2    MOV    1    0    'R1'
##    0x8A    2    MOV    1    0    'R2'
##    0x8B    2    MOV    1    0    'R3'
##    0x8C    2    MOV    1    0    'R4'
##    0x8D    2    MOV    1    0    'R5'
##    0x8E    2    MOV    1    0    'R6'
##    0x8F    2    MOV    1    0    'R7'
                case '@R0':
                    print('0x86', arg1)
                case '@R1':
                    print('0x87', arg1)
                case 'R0':
                    print('0x88', arg1)
                case 'R1':
                    print('0x89', arg1)
                case 'R2':
                    print('0x8A', arg1)
                case 'R3':
                    print('0x8B', arg1)
                case 'R4':
                    print('0x8C', arg1)
                case 'R5':
                    print('0x8D', arg1)
                case 'R6':
                    print('0x8E', arg1)
                case 'R7':
                    print('0x8F', arg1)
##     0x92    2    MOV    1    0    'C'
                case 'C':
                    print('0x92', arg1)

                case _:
##    0x75    3    MOV data addr    1    1    '#'
##    0x85    3    MOV              1    1    ''
                    if arg2.startswith('#'):
                        print('0x75', arg1, arg2[1:]) #  #0x75 -->0x75
                    else:
                        print('0x85', arg1, arg2) #


def assembly(line):
    instruction = line.strip().split()[0]
    match instruction:
        case instruction if instruction in clear:
            op_clear(line)
        case instruction if instruction in light:
            op_light(line)
        case instruction if instruction  in middle:
            op_middle(line)
        case instruction if instruction in hard:
            op_hard(line)


def main(asm_file):
    with open(asm_file, "r") as file:
        for line in file:
            line = line.strip()
            assembly(line)

if __name__ == '__main__':
    main(asm_file = 'test.asm')
