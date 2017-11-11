import os
import platform
import struct


class BasicDbReader:
    def __init__(self, file):
        """
        Initializes a BasicDbReader on the given file.
        :param file:
        """
        if not file or not os.path.exists(file):
            raise FileNotFoundError('Could not find from the specified file "%s"' % file)
        self.file = open(file, mode='rb')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

    def read_byte(self):
        """
        Read one Byte from the database-file
        :param file:
        :return:
        """
        return int.from_bytes(self.file.read(1), byteorder='little')

    def read_short(self):
        """
        Read a Short (2 Byte) from the database-file
        :return:
        """
        return int.from_bytes(self.file.read(2), byteorder='little')

    def read_int(self):
        """
        Read an Integer (4 Bytes) from the database-file
        :return:
        """
        return int.from_bytes(self.file.read(4), byteorder='little')

    def read_long(self):
        """
        Read a Long (8 bytes) from the database-file
        :return:
        """
        return int.from_bytes(self.file.read(8), byteorder='little')

    def read_uleb128(self):
        """
        Read a ULEB128 (variable) from the database-file
        :return:
        """
        result = 0
        shift = 0
        while True:
            byte = int.from_bytes(self.file.read(1), byteorder='little')
            result |= ((byte & 127) << shift)
            if (byte & 128) == 0:
                break
            shift += 7
        return result

    def read_single(self):
        """
        Read a Single (4 bytes) from the database-file
        :return:
        """
        return struct.unpack('f', self.file.read(4))

    def read_double(self):
        """
        Read a Double (8 bytes) from the database-file
        :return:
        """
        return struct.unpack('d', self.file.read(8))

    def read_boolean(self):
        """
        Read a Boolean (1 byte) from the database-file
        :return:
        """
        return self.read_byte() != 0

    def read_string(self):
        """
        Read a string (variable) from the database-file
        :return:
        """
        read = ''
        try:
            byte = self.read_byte()
            if byte == 0x0b:
                len = self.read_uleb128()
                read = self.file.read(len)
                return read.decode('utf8')
        except UnicodeDecodeError as e:
            print(len, read)
            raise e

    def read_datetime(self):
        """
        Read a Datetime from the database-file
        :return:
        """
        return self.read_long()

    def get_default_osu_path(self):
        osu_path = ''
        system = platform.system()

        if system == 'Windows':
            osu_path = os.path.join(os.getenv('LOCALAPPDATA'), 'osu!')  # Localapp
            if not os.path.exists(osu_path):
                osu_path = os.path.join(os.getenv('ProgramW6432'), 'osu!')  # "C:\Programm Files"
        elif system == 'Mac':
            osu_path = '/Applications/osu!.app/Contents/Resources/drive_c/Program Files/osu!/'

        if osu_path and os.path.exists(osu_path):
            return osu_path


class CollectionsDbReader(BasicDbReader):
    def __init__(self, file=None):
        # Tries to use a default file if the file was not specified or not found
        if not file or not os.path.exists(file):
            file = os.path.join(self.get_default_osu_path(), 'collection.db')
        super(CollectionsDbReader, self).__init__(file)
        self.version = self.read_int()
        self.num_collections = self.read_int()
        self._collections_read = 0

    def read_collection(self):
        if self._collections_read >= self.num_collections:
            return
        name = self.read_string()
        num_maps = self.read_int()
        md5_hashes = []

        for _ in range(num_maps):
            md5_hashes.append(self.read_string())

        self._collections_read += 1
        return {
            'name': name,
            'num_maps': num_maps,
            'md5_hashes': md5_hashes
        }

    def read_all_collections(self):
        collections = []
        for _ in range(self.num_collections):
            collections.append(self.read_collection())
        return collections


class OsuDbReader(BasicDbReader):
    def __init__(self, file=None):
        # Tries to use a default file if the file was not specified or not found
        if not file or not os.path.exists(file):
            file = os.path.join(self.get_default_osu_path(), 'osu!.db')
        super(OsuDbReader, self).__init__(file)
        self.version = self.read_int()
        self.folder_count = self.read_int()
        self.unlocked = self.read_boolean()
        self.date_unlocked = self.read_datetime()
        self.player = self.read_string()
        self.num_beatmaps = self.read_int()
        self._beatmap_read = 0

    def read_int_double_pair(self):
        """
        Read an int-double-pair (14 bytes) from the database-file
        :return:
        """
        if self.read_byte() == 0x08:
            first = self.read_int()
            if self.read_byte() != 0x0d:
                return first
            second = self.read_double()
            return first, second

    def _read_timingpoint(self):
        """
        Read a Timingpoint (17 bytes) from the database-file
        :return:
        """
        bpm = self.read_double()
        offset = self.read_double()
        inherited = self.read_boolean()

        return {
            'bpm': bpm,
            'offset': offset,
            'inherited': inherited
        }

    def read_beatmap(self):
        """
        Read one Beatmap from the database-file
        :return:
        """
        if self._beatmap_read >= self.num_beatmaps:
            return
        entry_size = self.read_int()
        artist = self.read_string()
        artist_unicode = self.read_string()
        title = self.read_string()
        title_unicode = self.read_string()
        creator = self.read_string()
        difficulty = self.read_string()
        audio_file = self.read_string()
        md5 = self.read_string()
        osu_file = self.read_string()
        ranked_status = self.read_byte()
        circle_count = self.read_short()
        slider_count = self.read_short()
        spinner_count = self.read_short()
        last_modification_time = self.read_long()
        ar = self.read_single()
        cs = self.read_single()
        hp = self.read_single()
        od = self.read_single()
        slider_velocity = self.read_double()

        # Difficulties in respect with the selected mod
        difficulties_std = []
        difficulties_taiko = []
        difficulties_ctb = []
        difficulties_mania = []

        length = self.read_int()
        for _ in range(length):
            difficulties_std.append(self.read_int_double_pair())

        length = self.read_int()
        for _ in range(length):
            difficulties_taiko.append(self.read_int_double_pair())

        length = self.read_int()
        for _ in range(length):
            difficulties_ctb.append(self.read_int_double_pair())

        length = self.read_int()
        for _ in range(length):
            difficulties_mania.append(self.read_int_double_pair())

        drain_time = self.read_int()
        total_time = self.read_int()
        preview_time = self.read_int()

        # Timingpoints
        timing_points = []
        length = self.read_int()
        for _ in range(length):
            timing_points.append(self._read_timingpoint())

        map_id = self.read_int()
        set_id = self.read_int()
        thread_id = self.read_int()
        grade_std = self.read_byte()
        grade_taiko = self.read_byte()
        grade_ctb = self.read_byte()
        grade_mania = self.read_byte()
        local_offset = self.read_short()
        stack_leniency = self.read_single()
        game_mode = self.read_byte()  # 0x00 = osu!Standard, 0x01 = Taiko, 0x02 = CTB, 0x03 = Mania
        song_source = self.read_string()
        song_tags = self.read_string()
        online_offset = self.read_short()
        font = self.read_string()  # Why do you even need this -_-
        unplayed = self.read_boolean()
        last_played = self.read_long()
        ignore_map_sound = self.read_boolean()
        ignore_map_skin = self.read_boolean()
        disable_storyboard = self.read_boolean()
        disable_video = self.read_boolean()
        visual_override = self.read_boolean()  # I have no idea what that is supposed to be
        last_modification_time_2 = self.read_int()  # I swear we had this already
        mania_scroll_speed = self.read_byte()

        self._beatmap_read += 1
        # Don't worry, I used multiply cursors to do within a minute
        return {
            'entry_size': entry_size,
            'artist': artist,
            'artist_unicode': artist_unicode,
            'title': title,
            'title_unicode': title_unicode,
            'creator': creator,
            'difficulty': difficulty,
            'audio_file': audio_file,
            'md5': md5,
            'osu_file': osu_file,
            'ranked_status': ranked_status,
            'circle_count': circle_count,
            'slider_count': slider_count,
            'spinner_count': spinner_count,
            'last_modification_time': last_modification_time,
            'ar': ar,
            'cs': cs,
            'hp': hp,
            'od': od,
            'slider_velocity': slider_velocity,
            'difficulties_std': difficulties_std,
            'difficulties_taiko': difficulties_taiko,
            'difficulties_ctb': difficulties_ctb,
            'difficulties_mania': difficulties_mania,
            'drain_time': drain_time,
            'total_time': total_time,
            'preview_time': preview_time,
            'timing_points': timing_points,
            'map_id': map_id,
            'set_id': set_id,
            'thread_id': thread_id,
            'grade_std': grade_std,
            'grade_taiko': grade_taiko,
            'grade_ctb': grade_ctb,
            'grade_mania': grade_mania,
            'local_offset': local_offset,
            'stack_leniency': stack_leniency,
            'game_mode': game_mode,
            'song_source': song_source,
            'song_tags': song_tags,
            'online_offset': online_offset,
            'font': font,
            'unplayed': unplayed,
            'last_played': last_played,
            'ignore_map_sound': ignore_map_sound,
            'ignore_map_skin': ignore_map_skin,
            'disable_storyboard': disable_storyboard,
            'disable_video': disable_video,
            'visual_override': visual_override,
            'last_modification_time_2': last_modification_time_2,
            'mania_scroll_speed': mania_scroll_speed
        }

    def read_all_beatmaps(self):
        beatmaps = []
        for _ in range(self.num_beatmaps):
            beatmaps.append(self.read_beatmap())
        return beatmaps


class ScoreDbReader(BasicDbReader):
    def __init__(self, file=None):
        # Tries to use a default file if the file was not specified or not found
        if not file or not os.path.exists(file):
            file = os.path.join(self.get_default_osu_path(), 'scores.db')
        super(ScoreDbReader, self).__init__(file)
        self.version = self.read_int()
        self.num_beatmaps = self.read_int()
        self._maps_read = 0

    def read_beatmap(self):
        if self._maps_read >= self.num_beatmaps:
            return
        md5 = self.read_string()
        score_count = self.read_int()
        scores = []
        for _ in range(score_count):
            scores.append(self._read_score())

        self._maps_read += 1
        return {
            'md5': md5,
            'score_count': score_count,
            'scores': scores
        }

    def _read_score(self):
        game_mode = self.read_byte()
        version = self.read_int()
        md5_beatmap = self.read_string()
        player = self.read_string()
        md5_replay = self.read_string()
        num_perfect = self.read_short()
        num_good = self.read_short()
        num_bad = self.read_short()
        num_geki = self.read_short()
        num_katus = self.read_short()
        num_miss = self.read_short()
        score_value = self.read_int()  # smh, still using integer
        max_combo = self.read_short()
        perfect = self.read_boolean()
        mods = self.read_boolean()
        unknown_empty = self.read_string()  # smh
        timestamp = self.read_long()
        unknown_minus_1 = self.read_int()
        online_score_id = self.read_long()

        return {
            'game_mode': game_mode,
            'version': version,
            'md5_beatmap': md5_beatmap,
            'player': player,
            'md5_replay': md5_replay,
            'num_perfect': num_perfect,
            'num_good': num_good,
            'num_bad': num_bad,
            'num_geki': num_geki,
            'num_katus': num_katus,
            'num_miss': num_miss,
            'score_value': score_value,
            'max_combo': max_combo,
            'perfect': perfect,
            'mods': mods,
            'unknown_empty': unknown_empty,
            'timestamp': timestamp,
            'unknown_minus_1': unknown_minus_1,
            'online_score_id': online_score_id
        }

    def read_all_beatmaps(self):
        beatmaps = []
        for _ in range(self.num_beatmaps):
            beatmaps.append(self.read_beatmap())
        return beatmaps
