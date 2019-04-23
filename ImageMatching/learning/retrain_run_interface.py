# -*- coding: utf-8 -*-

"""Inception v3 architecture 모델을 retraining한 모델을 이용해서 이미지에 대한 추론(inference)을 진행하는 예제"""

import numpy as np
import tensorflow as tf
import math
import operator
import os

# imagePath = '1e9b20b84b8f197e22fc7dc8578feb31.jpg'                                    # 추론을 진행할 이미지 경로
modelFullPath = './learning/output_graph.pb'                                      # 읽어들일 graph 파일 경로
labelsFullPath = './learning/output_labels.txt'                                   # 읽어들일 labels 파일 경로


def create_graph():
    """저장된(saved) GraphDef 파일로부터 graph를 생성하고 saver를 반환한다."""
    # 저장된(saved) graph_def.pb로부터 graph를 생성한다.
    with tf.gfile.FastGFile(modelFullPath, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')


def run_inference_on_image(imagePath):
    answer = None

    """if not tf.gfile.Exists(imagePath):
        tf.logging.fatal('File does not exist %s', imagePath)
        return answer"""

    tf.reset_default_graph()
    image_data = tf.gfile.FastGFile(imagePath, 'rb').read()
    create_graph()

    # 저장된(saved) GraphDef 파일로부터 graph를 생성한다.
    with tf.Session() as sess:

        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        predictions = sess.run(softmax_tensor,
                               {'DecodeJpeg/contents:0': image_data})
        predictions = np.squeeze(predictions)

        top_k = predictions.argsort()[-1:][::-1]  # 가장 높은 확률을 가진 5개(top 5)의 예측값(predictions)을 얻는다.
        f = open(labelsFullPath, 'rb')
        lines = f.readlines()
        labels = [str(w).replace("\n", "") for w in lines]
        file_path = ''
        for node_id in top_k:
            human_string = labels[node_id]
            if 'slacks' in human_string: file_path = 'slacks'
            elif 'jeans' in human_string: file_path = 'jeans'
            elif 'padding' in human_string: file_path = 'padding'
            elif 'jacket' in human_string: file_path = 'jacket'
            elif 'coat' in human_string: file_path = 'coat'
            elif 'top' in human_string: file_path = 'top'
            elif 'sweathers' in human_string: file_path = 'sweathers'
            elif 'shirts' in human_string: file_path = 'shirts'
            elif 'cardigan' in human_string: file_path = 'cardigan'
            score = predictions[node_id]
            print('%s (score = %.5f)' % (human_string, score))

        dictionary = np.load('./learning/%s_score.npy' % file_path).item()
        for key, value in dictionary.items():
            dictionary[key] = math.fabs(value - score)

        sorted_dict = sorted(dictionary.items(), key=operator.itemgetter(1))
        info = []
        for i in range(0, 16):
            info.append('./Images/use_images/train/' + file_path + '/%s' % (sorted_dict[i][0]))

        return file_path, info


"""if __name__ == '__main__':
    run_inference_on_image()"""