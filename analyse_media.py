#!/usr/bin/env python

import pymediainfo
import os

# media_path = "/Users/vinz/Documents/Media_scan/TV-SHOWS-Real/That '70s Show/S01/That.'70s.Show.S01.E01.DVD-Towel.mkv"

def media_info(db_collection):

    for media_path in db_collection.distinct("full_path"):

        from pymediainfo import MediaInfo
        media_info = MediaInfo.parse(media_path)

        if (len(list(media_info.tracks))) == 1:
            file_name = os.path.basename(media_path)
            print(f'--------------------\n!Warning! The following file does not have any track:\n{file_name}')
        else:
            audio_en, audio_fr, subs_en, subs_fr = ("no",)*4
            for track in media_info.tracks:

                if track.track_type == 'Video':
                    resolution = track.height
                    video_codec = track.codec_id

                if track.track_type == 'Audio':
                    if track.language == 'en': audio_en = "yes"
                    if track.language == 'fr': audio_fr = "yes"


                if track.track_type == 'Text':
                    if track.language == 'en': audio_en = "yes"
                    if track.language == 'fr': audio_fr = "yes"

        media_dict = { "resolution": resolution, "video_codec": video_codec, "audio_en": audio_en, "audio_fr": audio_fr, "subs_en": subs_en, "subs_fr": subs_fr }

        db_collection.update({"full_path": media_path}, {"$set": (media_dict)})


if __name__ == "__main__":
    media_info(db_collection)
