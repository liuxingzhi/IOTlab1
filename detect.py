from utils import visualization_utils as vis_util
from utils import label_map_util
import tensorflow as tf
import cv2
import numpy as np


class Detect:
    pb_path = 'ssd_mobilenet_v2.pb'
    label_path = 'label_map.pbtxt'

    def __init__(self):
        print("Initializing graph")
        with tf.device('gpu:0'):
            self.classes = label_map_util.create_category_index_from_labelmap(self.label_path, use_display_name=True)
            with tf.io.gfile.GFile(self.pb_path, 'rb') as fid:
                graph = tf.Graph()
                with graph.as_default():
                    graph_def = tf.GraphDef()
                    graph_def.ParseFromString(fid.read())
                    tf.import_graph_def(graph_def, name='')
            ops = graph.get_operations()
            all_tensor_names = {output.name for op in ops for output in op.outputs}
            self.tensor_dict = {}
            for key in [
                'num_detections', 'detection_boxes', 'detection_scores',
                'detection_classes', 'detection_masks'
            ]:
                tensor_name = key + ':0'
                if tensor_name in all_tensor_names:
                    self.tensor_dict[key] = graph.get_tensor_by_name(tensor_name)
            self.input_tensor = graph.get_tensor_by_name('image_tensor:0')
            self.sess = tf.Session(graph=graph)

    def _detect(self, img):
        output_dict = self.sess.run(self.tensor_dict, feed_dict={self.input_tensor: img})
        output_dict['num_detections'] = int(output_dict['num_detections'][0])
        output_dict['detection_classes'] = output_dict['detection_classes'][0].astype(np.int64)
        output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
        output_dict['detection_scores'] = output_dict['detection_scores'][0]
        return output_dict

    def show_detected_img(self, img_data, min_threshold=0.3):
        img = cv2.cvtColor(img_data, cv2.COLOR_BGR2RGB)
        img = np.array([img])
        output_dict = self._detect(img)
        img = img[0]
        return vis_util.visualize_boxes_and_labels_on_image_array(
            img,
            output_dict['detection_boxes'],
            output_dict['detection_classes'],
            output_dict['detection_scores'],
            self.classes,
            min_score_thresh=min_threshold,
            use_normalized_coordinates=True,
            line_thickness=3)

    def _wrap_detect(self, img, label):
        processed_img, cls = self.show_detected_img(img_data=img)
        return processed_img, label in cls.keys()

    def detect(self, img, label='person'):
        if isinstance(img, str):
            img = cv2.imread(img)
        return self._wrap_detect(img, label)

    def __enter__(self):
        return self

    def __exit__(self):
        self.sess.close()


if __name__ == '__main__':
    print("Detect object")
    # with Detect() as detect:
    #     print("Start inference")
    #     detect.detect(img=)
