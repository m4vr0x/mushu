#!/usr/bin/env python

import pymediainfo
import os
import logging

def media_info(db_collection):

    for media_path in db_collection.distinct("full_path"):

        mesg = (f'File analysed: {media_path}'); logging.info(mesg)

        from pymediainfo import MediaInfo
        media_info = MediaInfo.parse(media_path)

        if (len(list(media_info.tracks))) == 1:
            file_name = os.path.basename(media_path)
            mesg = (f'No track found for this file:\n\t{file_name}'); logging.warning(mesg)

        else:
            audio_en, audio_fr, subs_en, subs_fr = ('no',)*4
            audio_status, subs_status =  ('blank',)*2

            for track in media_info.tracks:

                # mesg = (f'{track}')
                mesg = (f'Track found with ID {track.track_id} and type {track.track_type}')
                logging.info(mesg)

                mesg = track.to_data(); logging.debug(f'Track raw data\n\t{mesg}')

                if track.track_type == 'Video':
                    resolution = track.height
                    video_codec = track.codec_id
                    mesg = (f'\n\tresolution = {resolution} and video_codec = {video_codec}'); logging.debug(mesg)

                if track.track_type == 'Audio':
                    if track.language == 'en': audio_en = "yes"
                    if track.language == 'fr': audio_fr = "yes"
                    mesg = (f'track.language = {track.language}'); logging.debug(mesg)
                    mesg = (f'audio_en = {audio_en} and audio_fr = {audio_fr}'); logging.debug(mesg)

                if track.track_type == 'Text':
                    if track.language == 'en': subs_en = "yes"
                    if track.language == 'fr': subs_fr = "yes"
                    mesg = (f'track.language = {track.language}'); logging.debug(mesg)
                    mesg = (f'subs_en = {subs_en} and subs_fr = {subs_fr}'); logging.debug(mesg)

        if (audio_en == "yes" and audio_fr == "yes"): audio_status = 'green'
        elif (audio_en == "no" and audio_fr == "no"): audio_status = 'red'
        elif (audio_en == "no" or audio_fr == "no"): audio_status = 'yellow'
        else:
            mesg = (f'No color defined for audio:\n\taudio_en = {audio_en}\n\taudio_fr = {audio_fr}'); logging.warning(mesg)
            pass

        if (subs_en == "yes" and subs_fr == "yes"): subs_status = 'green'
        elif (subs_en == "no" and subs_fr == "no"): subs_status = 'red'
        elif (subs_en == "no" or subs_fr == "no"): subs_status = 'yellow'
        else:
            mesg = (f'No color defined for subs:\n\tsubs_en = {subs_en}\n\tsubs_fr = {subs_fr}'); logging.warning(mesg)
            pass

        tracks_dict = { "resolution": resolution, "video_codec": video_codec, "audio_en": audio_en, "audio_fr": audio_fr, "subs_en": subs_en, "subs_fr": subs_fr, "audio_status": audio_status, "subs_status": subs_status }
        #
        # mesg = (f'tracks_dict =\n\t{tracks_dict}'); logging.debug(mesg)

        mesg = 'tracks_dict content:'
        for key, value in tracks_dict.items(): mesg += (f'\n\t{key}= {value}')
        logging.debug(mesg)

        db_collection.update({"full_path": media_path}, {"$set": (tracks_dict)})

if __name__ == "__main__":
    media_info(db_collection)
