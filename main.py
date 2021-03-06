# Resources
# https://towardsdatascience.com/how-to-detect-objects-in-real-time-using-opencv-and-python-c1ba0c2c69c0
# https://www.geeksforgeeks.org/feature-matching-using-orb-algorithm-in-python-opencv/
# https://blog.francium.tech/feature-detection-and-matching-with-opencv-5fd2394a590
# https://www.geeksforgeeks.org/feature-detection-and-matching-with-opencv-python/

# ORB: https://docs.opencv.org/3.4/d1/d89/tutorial_py_orb.html
# ORB feature matching:
# https://docs.opencv.org/3.4/dc/dc3/tutorial_py_matcher.html

import cv2
import time
from monkdetect.helpers import (
    gen_source_objs
)

def main():
    # generate source objects
    l_src_objs = gen_source_objs(source_dir='source')

    # define a video capture object
    vid = cv2.VideoCapture(0)
    vid.set(3, 800) # set width
    vid.set(4, 600) # set height

    orb = cv2.ORB_create(nfeatures=500)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    # change cycle
    while(True):
        ts = time.time() # bench mark

        ret, frame = vid.read()  # capture vid frame
        kp2, des2 = orb.detectAndCompute(frame, None)
        for src_obj in l_src_objs:
            kp1 = src_obj.kp
            des1 = src_obj.des
            source = src_obj.source
            try:  # try except because bf.match will raise an error if there is no match
                matches = bf.match(des1, des2)
                matches = sorted(matches, key=lambda x: x.distance)
                match_img = cv2.drawMatches(source, kp1, frame, kp2, matches[:50], None)

                # update score
                src_obj.append_score(len(matches))

                # Display the resulting frame
                cv2.imshow('Matches', match_img)
            except Exception as e:
                print(e)
                cv2.imshow('Matches', frame)
        fps = 1 / (time.time() - ts)

        # print scores
        l_src_objs = sorted(l_src_objs, key=lambda x: x.curr_avg_score)
        for src_obj in l_src_objs:
            print(f'{src_obj.path}: {src_obj.curr_avg_score:.0f}')
        print('-'*20)
        print(f'{fps:.0f} fps')
        print(f'Detected: {l_src_objs[-1].path}')
        print('-'*20)

        # Press q to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
