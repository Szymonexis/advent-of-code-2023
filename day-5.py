from typing import List, Tuple, TypedDict
from utils import clear_log, get_lines, log, log_table, profiler


class Vector(TypedDict):
    d: int
    s: int
    r: int
    o: int


VectorMap = Tuple[str, List[Vector]]


class SeedsAndVectorMaps(TypedDict):
    seeds: list[int]
    vector_maps: list[VectorMap]


def get_seeds(line: str) -> list[int]:
    return list(map(int, map(str.strip, line.split(':')[1].strip().split(' '))))


def get_map(lines: list[str], name: str) -> VectorMap:
    vectors: list[Vector] = []
    for line in lines:
        [d, s, r] = list(map(int, map(str.strip, line.strip().split(' '))))
        vectors.append(Vector(d=d, s=s, r=r, o=d-s))

    return (name, sorted(vectors, key=lambda x: x['s']))


def get_seeds_and_vector_maps() -> SeedsAndVectorMaps:
    lines = get_lines(__file__)
    seeds = sorted(get_seeds(lines[0]))

    section_indexes = []
    off = 3
    for i in range(off, len(lines[off:])):
        if lines[i] == '':
            section_indexes.append(i)
    section_indexes.append(len(lines))

    vector_maps: list[VectorMap] = []
    start = 1
    for section_index in section_indexes:
        map_lines = lines[start + 2:section_index]
        vector_maps.append(get_map(map_lines, lines[start + 1]))
        start = section_index

    return SeedsAndVectorMaps(seeds=seeds, vector_maps=vector_maps)


@profiler
def part_one():
    m = get_seeds_and_vector_maps()
    seeds = m['seeds']
    vector_maps = m['vector_maps']
    targets = seeds
    for (name, vectors) in vector_maps:
        i = 0
        j = 0
        n_ts = []
        vul = len(vectors) - 1
        while i < len(targets):
            v = vectors[j]
            d = v['d']
            s = v['s']
            o = v['o']
            r = v['r']
            e = s + r
            t = targets[i]

            t_smaller_than_v = t < s
            t_in_range_v = s <= t and t < e
            t_bigger_than_v = e <= t

            if t_smaller_than_v:
                n_ts.append(t)
                i += 1
                continue

            if t_in_range_v:
                n_ts.append(t + o)
                i += 1
                continue

            if t_bigger_than_v:
                if j < vul:
                    j += 1
                    continue

                if j == vul:
                    n_ts.append(t)
                    i += 1
                    continue

        targets = sorted(n_ts)

    min_location = min(targets)
    print(f'min_location: {min_location}')


class SeedRangesAndVectorMaps(TypedDict):
    seed_ranges: list[tuple[int, int]]
    vector_maps: list[VectorMap]


def get_seed_ranges(line: str) -> list[tuple[int, int]]:
    seeds = get_seeds(line)

    seed_ranges: list[tuple[int, int]] = []
    for i in range(0, len(seeds), 2):
        seed_ranges.append((seeds[i], seeds[i+1]))

    return seed_ranges


def get_seed_ranges_and_vector_maps() -> SeedRangesAndVectorMaps:
    lines = get_lines(__file__)
    seed_ranges = get_seed_ranges(lines[0])

    section_indexes = []
    off = 3
    for i in range(off, len(lines[off:])):
        if lines[i] == '':
            section_indexes.append(i)
    section_indexes.append(len(lines))

    vector_maps: list[VectorMap] = []
    start = 1
    for section_index in section_indexes:
        map_lines = lines[start + 2:section_index]
        vector_maps.append(get_map(map_lines, lines[start + 1]))
        start = section_index

    return SeedsAndVectorMaps(seed_ranges=seed_ranges, vector_maps=vector_maps)


def merge_ranges(ranges: list[tuple[int, int]]):
    # Filter out invalid ranges and transform into start-end format
    processed_ranges = [(start, start + length - 1)
                        for start, length in ranges if length > 0]

    # Sort the ranges based on start values
    processed_ranges.sort(key=lambda x: x[0])

    merged_ranges = []
    for current in processed_ranges:
        if not merged_ranges or current[0] > merged_ranges[-1][1] + 1:
            # If there is no overlap, add the current range as a new range
            merged_ranges.append(current)
        else:
            # If there is an overlap, merge the current range with the last added range
            merged_ranges[-1] = (merged_ranges[-1][0],
                                 max(merged_ranges[-1][1], current[1]))

    # Convert back to your desired format (start, length)
    return sorted([(start, end - start + 1) for start, end in merged_ranges], key=lambda x: x[0])


@profiler
def part_two():
    m = get_seed_ranges_and_vector_maps()
    seed_ranges = merge_ranges(m['seed_ranges'])
    vector_maps = m['vector_maps']

    targets = seed_ranges
    min_location = min(targets, key=lambda x: x[0])
    for (name, vectors) in vector_maps:
        j = 0
        n_ts: list[tuple[int, int]] = []
        vul = len(vectors) - 1
        while len(targets) != 0:
            v = vectors[j]
            d = v['d']
            s = v['s']
            o = v['o']
            r = v['r']
            e = s + r

            t = targets.pop(0)
            t_s = t[0]
            t_e = t[0] + t[1] - 1

            t_s_smaller_than_v = t_s < s
            t_s_in_range_v = s <= t_s and t_s < e
            t_s_bigger_than_v = e <= t_s

            t_e_smaller_than_v = t_e < s
            t_e_in_range_v = s <= t_e and t_e < e
            t_e_bigger_than_v = e <= t_e

            if t_s_smaller_than_v:
                # no new ranges
                if t_e_smaller_than_v:
                    n_ts.append((t_s, t_e - t_s))
                    continue

                # one new range at s
                if t_e_in_range_v:
                    n_t_smaller = (t_s, s - t_s)
                    n_t_in_range = (s + o, t_e - s)
                    n_ts.append(n_t_smaller)
                    n_ts.append(n_t_in_range)
                    continue

                # tow new ranges at s and e
                if t_e_bigger_than_v:
                    n_t_smaller = (t_s, s - t_s)
                    n_t_in_range = (s + o, e - s)
                    n_t_bigger = (e, t_e - e)
                    n_ts.append(n_t_smaller)
                    n_ts.append(n_t_in_range)
                    # cant be added to n_ts - need to add back to targets
                    targets.append(n_t_bigger)
                    targets = merge_ranges(targets)
                    continue

            if t_s_in_range_v:
                # whole target in range
                if t_e_in_range_v:
                    n_ts.append((t_s + o, t_e - t_s))
                    continue

                # two new ranges
                if t_e_bigger_than_v:
                    n_t_in_range = (t_s, e - t_s)
                    n_t_bigger = (e, t_e - e)
                    n_ts.append(n_t_in_range)
                    # cant be added to n_ts - need to add back to targets
                    targets.append(n_t_bigger)
                    targets = merge_ranges(targets)
                    continue

            if t_s_bigger_than_v:
                if j < vul:
                    j += 1
                    continue

                if j == vul:
                    n_ts.append((t_s, t_e - t_s))
                    continue

        targets = merge_ranges(n_ts)
        comp = []
        comp.append(min_location)
        for t in targets:
            comp.append(t)
        min_location = min(comp, key=lambda x: x[0])

    print(f'min_location: {min_location}')


part_one()
part_two()
