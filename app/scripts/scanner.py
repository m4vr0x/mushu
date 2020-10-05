# import os
import logging
from pymediainfo import MediaInfo

def media_info(collection, media_path):
        logging.info(f'File analysed: {media_path}')
        media_info = MediaInfo.parse(media_path)

        if (len(list(media_info.tracks))) == 1:
            # file_name = os.path.basename(media_path)
            file_name = media_path.rsplit('/',1)[1]
            logging.warning(f'No track found for this file: {file_name}')
        else:
            audio_en, audio_fr, subs_en, subs_fr = ('no',)*4
            audio_status, subs_status =  ('blank',)*2

            for track in media_info.tracks:
                # logging.info(f'Track found with ID: {track.track_id} and type: {track.track_type}')
                # raw_data = track.to_data()
                # logging.debug(f'Track raw data:\n\t{raw_data}')

                if track.track_type == 'Video':
                    resolution = track.height
                    video_codec = track.codec_id
                    logging.debug(f'Video track found with resolution: {resolution} and video_codec: {video_codec}')

                if track.track_type == 'Audio':
                    if track.language == 'en':
                        audio_en = "yes"
                        logging.debug(f'French audio track found')
                    elif track.language == 'fr':
                        audio_fr = "yes"
                        logging.debug(f'English audio track found')

                if track.track_type == 'Text':
                    if track.language == 'en':
                        subs_en = "yes"
                        logging.debug(f'French subtitle track found')
                    elif track.language == 'fr':
                        subs_fr = "yes"
                        logging.debug(f'English subtitle track found')


        tracks_dict = { "resolution": resolution, "video_codec": video_codec, "audio_en": audio_en, "audio_fr": audio_fr, "subs_en": subs_en, "subs_fr": subs_fr, "audio_status": audio_status, "subs_status": subs_status }
        # logging.debug(f'tracks_dict = {tracks_dict}')
        collection.update({"full_path": media_path}, {"$set": (tracks_dict)})

def languages_info(collection):

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
