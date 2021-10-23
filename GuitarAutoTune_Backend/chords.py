def frequency(referenceFrequency, semitonesDifference):
    return referenceFrequency * pow(2, (semitonesDifference / 12))


referencePitch = 440

STANDARD_TONES = {
    'E4': frequency(referencePitch, -5.000),
    'H3': frequency(referencePitch, -10.000),
    'G3': frequency(referencePitch, -14.000),
    'D3': frequency(referencePitch, -19.000),
    'A2': frequency(referencePitch, -24.000),
    'E2': frequency(referencePitch, -29.000),
}

# http://www.gitarre-stimmen.de/html/open_d.html
OPEN_D_TONES = {
    'D4': frequency(referencePitch, -7.000),
    'A3': frequency(referencePitch, -12.000),
    'F#3': frequency(referencePitch, -15.000),
    'D3': frequency(referencePitch, -19.000),
    'A2': frequency(referencePitch, -24.000),
    'D2': frequency(referencePitch, -31.000),
}

# http://www.gitarre-stimmen.de/html/open_d_moll.html
OPEN_D_MOLL_TONES = {
    'D4': frequency(referencePitch, -7.000),
    'A3': frequency(referencePitch, -12.000),
    'F3': frequency(referencePitch, -16.000),
    'D3': frequency(referencePitch, -19.000),
    'A2': frequency(referencePitch, -24.000),
    'D2': frequency(referencePitch, -31.000),
}
