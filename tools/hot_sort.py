#-*-coding=utf-8-*-
"""热度排序
"""

media_weight = {}
f = open('media')
def get_media_weight(media):
	w = 1
	if media in media_weight.keys():
		w = media_weight['media']

	return w