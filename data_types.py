from typing import Dict, List, Optional, TypedDict, Union


class Disposition(TypedDict):
    default: int
    dub: int
    original: int
    comment: int
    lyrics: int
    karaoke: int
    forced: int
    hearing_impaired: int
    visual_impaired: int
    clean_effects: int
    attached_pic: int
    timed_thumbnails: int
    non_diegetic: int
    captions: int
    descriptions: int
    metadata: int
    dependent: int
    still_image: int


class Tags(TypedDict):
    creation_time: str
    language: str
    handler_name: str
    vendor_id: str
    encoder: str


class Stream(TypedDict):
    index: int
    codec_name: str
    codec_long_name: str
    codec_type: str
    codec_tag_string: str
    codec_tag: str
    width: int
    height: int
    coded_width: Optional[int]
    coded_height: Optional[int]
    closed_captions: Optional[int]
    film_grain: Optional[int]
    has_b_frames: Optional[int]
    pix_fmt: str
    level: int
    chroma_location: Optional[str]
    field_order: Optional[str]
    refs: int
    is_avc: Optional[str]
    nal_length_size: Optional[str]
    id: Optional[str]
    r_frame_rate: str
    avg_frame_rate: str
    time_base: str
    start_pts: Optional[int]
    start_time: Optional[str]
    duration_ts: Optional[int]
    duration: Optional[str]
    bit_rate: Optional[Union[int, str]]
    bits_per_raw_sample: Optional[Union[int, str]]
    nb_frames: Optional[str]
    extradata_size: Optional[int]
    disposition: Disposition
    tags: Optional[Dict[str, str]]
    color_range: Optional[str]
    color_space: Optional[str]
    color_transfer: Optional[str]
    color_primaries: Optional[str]


# Define type for the root dictionary
class VideoInfo(TypedDict):
    streams: List[Stream]
