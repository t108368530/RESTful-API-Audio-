import numpy as np

import librosa


def extract_Features(data) -> np.ndarray:
    try:
        X, sampleRate = librosa.load(
            data,
            sr=None,
            offset=0.0,
            res_type="kaiser_best",
            dtype=np.float32,
        )
        spectral_contrast_fmin = 0.5 * sampleRate * 2 ** (-6)
        if sampleRate < 8000:
            spectral_contrast_fmin = 200
        mel = np.mean(librosa.feature.melspectrogram(X, sr=sampleRate).T, axis=0)
        tonnetz = np.mean(
            librosa.feature.tonnetz(y=librosa.effects.harmonic(X), sr=sampleRate).T,
            axis=0,
        )
        mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sampleRate, n_mfcc=40).T, axis=0)
        mfcc_delta = librosa.feature.delta(mfccs)  # TONY
        mfcc_delta2 = librosa.feature.delta(mfccs, order=2)  # TONY
        stft = np.abs(librosa.stft(X))
        chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sampleRate).T, axis=0)
        contrast = np.mean(
            librosa.feature.spectral_contrast(
                S=stft, sr=sampleRate, fmin=spectral_contrast_fmin
            ).T,
            axis=0,
        )

        ###### ADD NEW FEATURES (SPECTRAL RELATED)##### 24-SEP
        cent = np.mean(librosa.feature.spectral_centroid(y=X, sr=sampleRate).T, axis=0)
        flatness = np.mean(librosa.feature.spectral_flatness(y=X).T, axis=0)
        rolloff = np.mean(
            librosa.feature.spectral_rolloff(S=stft, sr=sampleRate).T, axis=0
        )
        rms = np.mean(librosa.feature.rms(S=stft).T, axis=0)
        ext_features = np.hstack(
            [
                mfccs,
                mfcc_delta,
                mfcc_delta2,
                chroma,
                mel,
                contrast,
                tonnetz,
                cent,
                flatness,
                rolloff,
                rms,
            ]
        )
    except Exception as e:
        print("Error : %s" % e)
        return None

    return np.array(ext_features)


def make_spec(data, st=4)-> np.ndarray:
    sig, rate = librosa.load(data, sr=16000)
    if len(sig) < 16000:  # pad shorter than 1 sec audio with ramp to zero
        sig = np.pad(sig, (0, 16000 - len(sig)), "linear_ramp")
    D = librosa.amplitude_to_db(
        librosa.stft(sig[:16000], n_fft=512, hop_length=128, center=False), ref=np.max
    )
    S = librosa.feature.melspectrogram(S=D, n_mels=85).T
    S = np.ascontiguousarray(S,dtype=np.float32)
    return np.expand_dims(S,-1)+1.3