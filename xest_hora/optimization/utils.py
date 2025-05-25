def unique(my_list: list | chain[tuple[Any, Any]] | Generator) -> list:
    """Get the unique values of a list keeping the order in which the elements appear.

    Args:
        my_list (list | chain[tuple[Any, Any]] | Generator): list with repeated elements.

    Returns:
        list: list without repeated elements.

    Example:
        >>> from optimization_autobots.domain.analysis.list_utils import unique
        >>> unique([1, "1", 2, 1, 3])
        [1, '1', 2, 3]
    """
    used = set()
    return [x for x in my_list if x not in used and (used.add(x) or True)]
