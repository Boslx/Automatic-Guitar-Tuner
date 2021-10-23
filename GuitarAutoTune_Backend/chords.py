def frequency(referenceFrequency, semitonesDifference):
    return referenceFrequency * pow(2, (semitonesDifference / 12))


referencePitch = 440

STANDARD_TONES = {
    'E2': frequency(referencePitch, -29.000),
    'A2': frequency(referencePitch, -24.000),
    'D3': frequency(referencePitch, -19.000),
    'G3': frequency(referencePitch, -14.000),
    'H3': frequency(referencePitch, -10.000),
    'E4': frequency(referencePitch, -5.000)
}

# http://www.gitarre-stimmen.de/html/open_d.html
OPEN_D_TONES = {
    'D2': frequency(referencePitch, -31.000),
    'A2': frequency(referencePitch, -24.000),
    'D3': frequency(referencePitch, -19.000),
    'F#3': frequency(referencePitch, -15.000),
    'A3': frequency(referencePitch, -12.000),
    'D4': frequency(referencePitch, -7.000),
}

# http://www.gitarre-stimmen.de/html/open_d_moll.html
OPEN_D_MOLL_TONES = {
    'D2': frequency(referencePitch, -31.000),
    'A2': frequency(referencePitch, -24.000),
    'D3': frequency(referencePitch, -19.000),
    'F3': frequency(referencePitch, -16.000),
    'A3': frequency(referencePitch, -12.000),
    'D4': frequency(referencePitch, -7.000),
}

# https://gtdb.org/cgcgce
# | Note                                     | Hz                                           |
# |------------------------------------------|----------------------------------------------|
# |                      C2                  |                      65.41                   |
# |                      G2                  |                      98.00                   |
# |                      C3                  |                      130.81                  |
# |                      G3                  |                      196.00                  |
# |                      C4                  |                      261.63                  |
# |                      E4                  |                      329.63                  |

OPEN_C_MAJOR = {
    'C2': 65.41,
    'G2': 98.00,
    'C3': 130.81,
    'G3': 196.00,
    'C4': 261.63,
    'E4': 329.63,
}

# https://gtdb.org/dgdgbd
# | Note                                     | Hz                                           |
# |------------------------------------------|----------------------------------------------|
# |                      D2                  |                      73.42                   |
# |                      G2                  |                      98.00                   |
# |                      D3                  |                      146.83                  |
# |                      G3                  |                      196.00                  |
# |                      B3                  |                      246.94                  |
# |                      D4                  |                      293.66                  |

OPEN_G_MAJOR = {
    'D2': 73.42,
    'G2': 98.00,
    'D3': 146.83,
    'G3': 196.00,
    'B3': 246.94,
    'D4': 293.66,
}

# https://gtdb.org/eaeace
# | Note                                     | Hz                                           |
# |------------------------------------------|----------------------------------------------|
# |                      E2                  |                      82.41                   |
# |                      A2                  |                      110.00                  |
# |                      E3                  |                      164.81                  |
# |                      A3                  |                      220.00                  |
# |                      C4                  |                      261.63                  |
# |                      E4                  |                      329.63                  |

OPEN_A_MINOR = {
    'E2': 82.41,
    'A2': 110.00,
    'E3': 164.81,
    'A3': 220.00,
    'C4': 261.63,
    'E4': 329.63,
}

# https://gtdb.org/cfcfac
# | Note                                     | Hz                                           |
# |------------------------------------------|----------------------------------------------|
# |                      C2                  |                      65.41                   |
# |                      F2                  |                      87.31                   |
# |                      C3                  |                      130.81                  |
# |                      F3                  |                      174.61                  |
# |                      A3                  |                      220.00                  |
# |                      C4                  |                      261.63                  |

OPEN_F_MAJOR = {
    'C2': 65.41,
    'F2': 87.31,
    'C3': 130.81,
    'F3': 174.61,
    'A3': 220.00,
    'C4': 261.63,
}

SONG = [
    OPEN_C_MAJOR,
    OPEN_G_MAJOR,
    OPEN_A_MINOR,
    OPEN_F_MAJOR
]


def getStringMission(song, string):
    stringMission = []
    for chord in song:
        stringMission.append(list(chord.values())[0])
    return stringMission
