from imageai.Detection import *
import cv2

class myDetector(ObjectDetection):

    def __init__(self):
        super().__init__()

    def detectObjectsFromVideo(self, input_file_path="", camera_input = None, output_file_path="", frames_per_second=20, frame_detection_interval=1, minimum_percentage_probability=50, log_progress=False, display_percentage_probability=True, display_object_name = True, save_detected_video = True, per_frame_function = None, per_second_function = None, per_minute_function = None, video_complete_function = None, return_detected_frame = False ):

            try:
                if(True):



                    input_video = cv2.VideoCapture(input_file_path)
                    if (camera_input != None):
                        input_video = camera_input


                    counting = 0
                    predicted_numbers = None
                    scores = None
                    detections = None

                    model = self.__model_collection[0]

                    while (input_video.isOpened()):
                        ret, frame = input_video.read()

                        if (ret == True):

                            output_objects_array = []

                            counting += 1

                            if (log_progress == True):
                                print("Processing Frame : ", str(counting))

                            detected_copy = frame.copy()
                            detected_copy = cv2.cvtColor(detected_copy, cv2.COLOR_BGR2RGB)

                            frame = preprocess_image(frame)
                            frame, scale = resize_image(frame, min_side=self.__input_image_min,
                                                        max_side=self.__input_image_max)

                            check_frame_interval = counting % frame_detection_interval

                            if (counting == 1 or check_frame_interval == 0):
                                _, _, detections = model.predict_on_batch(np.expand_dims(frame, axis=0))
                                predicted_numbers = np.argmax(detections[0, :, 4:], axis=1)
                                scores = detections[0, np.arange(detections.shape[1]), 4 + predicted_numbers]

                                detections[0, :, :4] /= scale

                            min_probability = minimum_percentage_probability / 100

                            for index, (label, score), in enumerate(zip(predicted_numbers, scores)):
                                if score < min_probability:
                                    continue

                                color = label_color(label)

                                detection_details = detections[0, index, :4].astype(int)
                                draw_box(detected_copy, detection_details, color=color)

                                if (display_object_name == True and display_percentage_probability == True):
                                    caption = "{} {:.3f}".format(self.numbers_to_names[label], (score * 100))
                                    draw_caption(detected_copy, detection_details, caption)
                                elif (display_object_name == True):
                                    caption = "{} ".format(self.numbers_to_names[label])
                                    draw_caption(detected_copy, detection_details, caption)
                                elif (display_percentage_probability == True):
                                    caption = " {:.3f}".format((score * 100))
                                    draw_caption(detected_copy, detection_details, caption)

                                each_object_details = {}
                                each_object_details["name"] = self.numbers_to_names[label]
                                each_object_details["percentage_probability"] = score * 100
                                each_object_details["box_points"] = detection_details
                                output_objects_array.append(each_object_details)

                            output_frames_dict[counting] = output_objects_array

                            output_objects_count = {}
                            for eachItem in output_objects_array:
                                eachItemName = eachItem["name"]
                                try:
                                    output_objects_count[eachItemName] = output_objects_count[eachItemName] + 1
                                except:
                                    output_objects_count[eachItemName] = 1

                            output_frames_count_dict[counting] = output_objects_count

                            detected_copy = cv2.cvtColor(detected_copy, cv2.COLOR_BGR2RGB)
                            cv2.imshow("myDetector",detected_copy)

                            if (per_frame_function != None):
                                if(return_detected_frame == True):
                                    per_frame_function(counting, output_objects_array, output_objects_count, detected_copy)
                                elif(return_detected_frame == False):
                                    per_frame_function(counting, output_objects_array, output_objects_count)

                            if (per_second_function != None):
                                if (counting != 1 and (counting % frames_per_second) == 0):

                                    this_second_output_object_array = []
                                    this_second_counting_array = []
                                    this_second_counting = {}

                                    for aa in range(counting):
                                        if (aa >= (counting - frames_per_second)):
                                            this_second_output_object_array.append(output_frames_dict[aa + 1])
                                            this_second_counting_array.append(output_frames_count_dict[aa + 1])

                                    for eachCountingDict in this_second_counting_array:
                                        for eachItem in eachCountingDict:
                                            try:
                                                this_second_counting[eachItem] = this_second_counting[eachItem] + \
                                                                                 eachCountingDict[eachItem]
                                            except:
                                                this_second_counting[eachItem] = eachCountingDict[eachItem]

                                    for eachCountingItem in this_second_counting:
                                        this_second_counting[eachCountingItem] = this_second_counting[
                                                                                     eachCountingItem] / frames_per_second


                                    if (return_detected_frame == True):
                                        per_second_function(int(counting / frames_per_second),
                                                            this_second_output_object_array, this_second_counting_array,
                                                            this_second_counting, detected_copy)

                                    elif (return_detected_frame == False):
                                        per_second_function(int(counting / frames_per_second),
                                                            this_second_output_object_array, this_second_counting_array,
                                                            this_second_counting)

                            if (per_minute_function != None):

                                if (counting != 1 and (counting % (frames_per_second * 60)) == 0):


                                    this_minute_output_object_array = []
                                    this_minute_counting_array = []
                                    this_minute_counting = {}

                                    for aa in range(counting):
                                        if (aa >= (counting - (frames_per_second * 60))):
                                            this_minute_output_object_array.append(output_frames_dict[aa + 1])
                                            this_minute_counting_array.append(output_frames_count_dict[aa + 1])

                                    for eachCountingDict in this_minute_counting_array:
                                        for eachItem in eachCountingDict:
                                            try:
                                                this_minute_counting[eachItem] = this_minute_counting[eachItem] + \
                                                                                 eachCountingDict[eachItem]
                                            except:
                                                this_minute_counting[eachItem] = eachCountingDict[eachItem]

                                    for eachCountingItem in this_minute_counting:
                                        this_minute_counting[eachCountingItem] = this_minute_counting[
                                                                                     eachCountingItem] / (frames_per_second * 60)


                                    if (return_detected_frame == True):
                                        per_minute_function(int(counting / (frames_per_second * 60)),
                                                            this_minute_output_object_array, this_minute_counting_array,
                                                            this_minute_counting, detected_copy)

                                    elif (return_detected_frame == False):
                                        per_minute_function(int(counting / (frames_per_second * 60)),
                                                            this_minute_output_object_array, this_minute_counting_array,
                                                            this_minute_counting)


                        else:
                            break


                return detected_copy


            except:
                raise ValueError("An error occured. It may be that your input video is invalid. Ensure you specified a proper string value for 'output_file_path' is 'save_detected_video' is not False. "
                                 "Also ensure your per_frame, per_second, per_minute or video_complete_analysis function is properly configured to receive the right parameters. ")



