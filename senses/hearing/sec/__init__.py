import os
import numpy as np
import resampy
import tensorflow as tf

import senses.hearing.sec.params as yamnet_params
import senses.hearing.sec.yamnet as yamnet_model


class SEC:
    def __init__(self):
        self.params = yamnet_params.Params()
        self.yamnet = yamnet_model.yamnet_frames_model(self.params)
        self.yamnet.load_weights(os.path.join(os.getcwd(), 'senses', 'hearing', 'sec', 'yamnet.h5'))
        self.yamnet_classes = yamnet_model.class_names(os.path.join(os.getcwd(), 'senses', 'hearing', 'sec', 'yamnet_class_map.csv'))

    def classify(self, wav_data, sr):
        assert wav_data.dtype == np.int16, 'Bad sample type: %r' % wav_data.dtype
        waveform = wav_data / 32768.0  # Convert to [-1.0, +1.0]
        waveform = waveform.astype('float32')

        # Convert to mono and the sample rate expected by YAMNet.
        if len(waveform.shape) > 1:
            waveform = np.mean(waveform, axis=1)
        if sr != self.params.sample_rate:
            waveform = resampy.resample(waveform, sr, self.params.sample_rate)

        # Predict YAMNet classes.
        scores, embeddings, spectrogram = self.yamnet(waveform)
        # Scores is a matrix of (time_frames, num_classes) classifier scores.
        # Average them along time to get an overall classifier output for the clip.
        prediction = np.mean(scores, axis=0)
        # Report the highest-scoring classes and their scores.
        top5_i = np.argsort(prediction)[::-1][:5]

        return self.yamnet_classes[top5_i[0]], self.yamnet_classes[top5_i[1]], self.yamnet_classes[top5_i[2]], self.yamnet_classes[top5_i[3]], self.yamnet_classes[top5_i[4]]
