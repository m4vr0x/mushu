#!/usr/bin/env python

import pymediainfo

media_path = "/Users/vinz/Documents/Media_scan/TV-SHOWS-Real/Young Sheldon/S01/Young.Sheldon.S01E02.Rockets.Communists.and.the.Dewey.Decimal.System.720p.AMZN.WEB-DL.DDP5.1.H.264-NTb.mkv"

def media_info(media_path):

    from pymediainfo import MediaInfo
    media_info = MediaInfo.parse(media_path)
    for track in media_info.tracks:
        # print(f'\n{track}')
        # print('--------------------')

        if track.track_type == 'General':
            print (track.complete_name)

        if track.track_type == 'Video':
            print (track.track_id, track.track_type, track.format, track.codec_id, track.height)

        if track.track_type == 'Audio':
            print (track.track_id, track.track_type, track.format, track.commercial_name, track.language)

        if track.track_type == 'Text':
            print (track.track_id, track.track_type, track.format, track.language)

media_info(media_path)
