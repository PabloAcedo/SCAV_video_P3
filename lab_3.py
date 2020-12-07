import os


# exercise 1 (all this was done inside the material folder)
# cut 1 min of video from original BBB
# ffmpeg -i bbb_original.mp4 -ss 00:00:00 -t 00:01:00 -an bbb_only_video.h264

# extract 1 min of audio from the video
# ffmpeg -i bbb_original.mp4 -ss 00:00:00 -t 00:01:00 -ac 1 bbb_audio_1min.mp3

# extract 1 min of audio at a lower sample rate
# ffmpeg -i bbb_original.mp4 -ss 00:00:00 -t 00:01:00 -b:a 32k -ac 1 bbb_audio_1min_32k.mp3

# create a new mp4 container from the extracted streams + subtitles ffmpeg -i bbb_only_video.h264 -i
# bbb_audio_1min.mp3 -i bbb_audio_1min_32k.mp3 -i bbb_1min.srt -map 0:v -map 1:a -map 2:a -map 3 -codec:a copy
# -codec:s mov_text new_bbb.mp4


class lab3:
    # function to, given a list of strings and a keyword, it says that if this keyword is inside this data
    def is_in_file(self, data_lines_container, keyword):
        # iterate over the list of data (lines from the txt containing the ffmpeg analysis)
        for i in range(len(data_lines_container)):
            # if found return true
            if data_lines_container[i].find(keyword) > -1:
                # print all the lines containing the keyword
                return True

        return False

    # exercise 2
    # function to create a mp4 container given the video and audio streams and the subtitles
    def create_mp4(self, video_stream, audio_stream_1, audio_stream_2, subtitles):
        # all the inputs are the file names
        os.system(
            'ffmpeg -i ' + video_stream + ' -i ' + audio_stream_1 + ' -i ' + audio_stream_2 + ' -i ' + subtitles +
            ' -map 0:v -map 1:a -map 2:a -map 3 -codec:a copy -codec:s mov_text material/new_bbb.mp4')

    # exercise 3
    # DVB: Video: MPEG2 (mpeg2video), h.264. Audio: aac, ac3, mp3, mp2, mp1.
    # ISDB: Video: MPEG2 (mpeg2video), h.264. Audio: aac.
    # ATSC: Video: MPEG2 (mpeg2video), h.264. Audio: ac3.
    # DTMB: Video: MPEG2 (mpeg2video), h.264, avs, avs+. Audio: aac, ac3, mp3, mp2, dra.
    def broadcasting_standard(self):
        # ffmpeg info to txt file
        order = 'ffmpeg -i material/new_bbb.mp4 2> material/output_data.txt'
        os.system(order)

        # read info in txt file
        f = open('material/output_data.txt', 'r')

        # convert lines of the txt file to list of str
        lines = f.readlines()

        f.close()

        keywords = ['mpeg2video', 'h264', 'avs', 'avs+', 'aac', 'ac3', 'mp3', 'mp2', 'mp1', 'dra']

        compatible = []  # array of booleans
        standards = []  # array of strings with the broadcasting standard names

        # check the broadcasting standards
        for keyword in keywords:
            compatible.append(self.is_in_file(lines, keyword))

        if compatible[4] or compatible[5] or compatible[6] or compatible[7] or compatible[8]:
            if compatible[0] or compatible[1]:
                standards.append('DVB')

        if compatible[4] or compatible[5] or compatible[6] or compatible[7] or compatible[9]:
            if compatible[0] or compatible[1] or compatible[2] or compatible[3]:
                standards.append('DTMB')

        if compatible[4]:
            if compatible[0] or compatible[1]:
                standards.append('ISDB')

        if compatible[5]:
            if compatible[0] or compatible[1]:
                standards.append('ATSC')

        if len(standards) > 0:
            print('\nCompatible broadcasting standards: ', standards)
        else:
            print('\nERROR, THIS VIDEO DOES NOT FIT ANY BROADCASTING STANDARD!')

    # exercise 4: create container and analyse it with the ex3 method
    def create_and_analyse(self):
        _cont = 'y'
        while _cont == 'y':
            print('\nThe video codec of the new container will always be h264.')  # fits in all the standards
            print('\nEnter the desired AUDIO codec for the new container: ')  # this will make the difference
            audio_codec = input()
            # extract/create new audio streams
            order = 'ffmpeg -i material/bbb_original.mp4 -ss 00:00:00 -t 00:01:00 -ac 1 material/bbb_audio_1min.' + audio_codec
            os.system(order)
            order = 'ffmpeg -i material/bbb_original.mp4 -ss 00:00:00 -t 00:01:00 -b:a 32k -ac 1 ' \
                    'material/bbb_audio_1min_32k.' + audio_codec
            os.system(order)
            # create the new container
            video_stream = 'material/bbb_only_video.h264'
            audio_1 = 'material/bbb_audio_1min.' + audio_codec
            audio_2 = 'material/bbb_audio_1min_32k.' + audio_codec
            subtitles = 'material/bbb_1min.srt'
            self.create_mp4(video_stream, audio_1, audio_2, subtitles)
            # check broadcasting standards for the new container
            self.broadcasting_standard()
            print('\nYou want to create and analyse another container?[y/n]')
            _cont = input()


# launch practise
obj = lab3()
obj.create_and_analyse()
