# Third party packages
from __future__ import annotations
import pandas as pd
from typing import Union

# Package modules
import logging as log


class Aggregation:
    """The Aggregation class is a general class to build and validate the data.

    NOTE: This class does not make a copy of the original pd.DataFrame in order to optimize memory usage.
    Be careful if you modify the pd.DataFrame.

    RECOMMENDATION: if you have to modify the original pd.DataFrame, recreate the Aggregation object with the
    modified pd.DataFrame.

    Attributes:
        _name (str): name of the aggregation.
        _columns (list): name of the columns of the DataFrame.
        _indices (list): unique index to determine a row in the DataFrame. It
            is equivalent to Primary Keys (PK) in the relational DB context.
        _required_columns (list): required columns of the DataFrame.
        _default_column_values (dict): default value for missing DataFrame
            columns.
        _columns_type (dict): type of the DataFrame columns.
        data (pd.DataFrame): aggregated data.

    Raises:
        ValueError: if missing required column.
        TypeError: invalid column type.
    """

    # TODO: Use sparse matrix to improve memory usage
    # (https://pandas.pydata.org/pandas-docs/stable/user_guide/sparse.html)

    _columns = []
    _indices = []
    _required_columns = []
    _default_column_values = {}
    _columns_type = {}

    def __init__(
        self,
        data: Union[pd.DataFrame, None] = None,
        sort: bool = True,
        drop_duplicates: bool = True,
        ignore_index: bool = True,
    ):
        """Initialize the Aggregation class.

        Args:
            data (Union[pd.DataFrame, None], optional): aggregated data. It must follow the structure defined by its
                columns, indices, required columns, and columns types. If None empty DataFrame is created. Defaults to
                None.
            sort (bool, optional): Boolean to indicate if is necessary sort the data or not. Defaults to True.
            drop_duplicates (bool, optional): Boolean to indicate if is necessary remove duplicated rows or not.
                Defaults to True.
            ignore_index (bool, optional): Boolean to indicate if is necessary ignore index or not. Defaults to True.

        Examples:
            Empty aggregation:

            >>> from optimization_autobots.domain.aggregation import Aggregation
            >>> aggregation = Aggregation()
            >>> aggregation
            Empty Aggregation

            Aggregation with data:

            >>> from optimization_autobots.domain.aggregation import Aggregation
            >>> import pandas as pd
            >>> aggregation = Aggregation(data=pd.DataFrame([{}]))
            >>> aggregation
            Empty DataFrame
            Columns: []
            Index: [0]
        """
        self._drop_duplicates = drop_duplicates
        self._sort = sort
        self._ignore_index = ignore_index
        self.data = data

    @property
    def data(self) -> pd.DataFrame:
        """Data information. Secure property that copies the data to prevent it
        from being modified in the original object.

        Returns:
            pd.DataFrame: data information.

        Examples:

            Getter example:

            >>> from optimization_autobots.domain.aggregation import Aggregation
            >>> import pandas as pd
            >>> aggregation = Aggregation(data=pd.DataFrame([{}]))
            >>> aggregation.data
            Empty DataFrame
            Columns: []
            Index: [0]

            Setter example:

            >>> from optimization_autobots.domain.aggregation import Aggregation
            >>> import pandas as pd
            >>> aggregation = Aggregation()
            >>> aggregation.data
            Empty DataFrame
            Columns: []
            Index: []
            >>> aggregation.data = pd.DataFrame([{}])
            >>> aggregation.data
            Empty DataFrame
            Columns: []
            Index: [0]

            Update data with an invalid object:

            >>> from optimization_autobots.domain.aggregation import Aggregation
            >>> aggregation = Aggregation()
            >>> invalid_data = {}
            >>> aggregation.data = invalid_data
            Traceback (most recent call last):
                ...
            TypeError: [Aggregation] Invalid data type: dict

            Missing required column:

            >>> from optimization_autobots.domain.aggregation import Aggregation
            >>> import pandas as pd
            >>> aggregation = Aggregation()
            >>> aggregation._columns = ['column1']
            >>> aggregation._required_columns = ['column1']
            >>> aggregation.data = pd.DataFrame([{}])
            Traceback (most recent call last):
                ...
            ValueError: [Aggregation] Required columns not found: column1

            Invalid column type:

            >>> from optimization_autobots.domain.aggregation import Aggregation
            >>> import pandas as pd
            >>> aggregation = Aggregation()
            >>> aggregation._columns = ['column1']
            >>> aggregation._indices = ['column1']
            >>> aggregation._columns_type = {'column1': int}
            >>> aggregation.data = pd.DataFrame([{'column1': 'a'}])
            Traceback (most recent call last):
                ...
            ValueError: invalid literal for int() with base 10: 'a'

            Invalid column but with known transformation to a valid type:

            >>> from optimization_autobots.domain.aggregation import Aggregation
            >>> import pandas as pd
            >>> aggregation = Aggregation()
            >>> aggregation._columns = ['column1']
            >>> aggregation._indices = ['column1']
            >>> aggregation._columns_type = {'column1': int}
            >>> aggregation.data = pd.DataFrame([{'column1': '1'}])
            >>> aggregation
               column1
            0        1

            Default values:

            >>> from optimization_autobots.domain.aggregation import Aggregation
            >>> import pandas as pd
            >>> aggregation = Aggregation()
            >>> aggregation._columns = ['index1', 'column1', 'column2']
            >>> aggregation._indices = ['index1']
            >>> aggregation._required_columns = ['index1']
            >>> aggregation._default_column_values = {'column1': 1, 'column2': 2}
            >>> aggregation._columns_type = {'index1': int, 'column1': int, 'column2': int}
            >>> aggregation.data = pd.DataFrame([
            ...     dict(index1=0, column1=1),
            ...     dict(index1=1, column1=2),
            ...     dict(index1=2),
            ... ])
            >>> aggregation
               index1  column1  column2
            0       0        1        2
            1       1        2        2
            2       2        1        2
        """
        return self.__data.copy()

    @property
    def _data(self):
        """Data information. Property not secure as data is not copied. IMPORTANT: only use it to query data.

        Returns:
            pd.DataFrame: data information.

        Examples:
            Safety cases where we could use the _data property to query data:

            1. When we filter the data, then a copy of the DataFrame is created. So it will be a safe operation as the
            original data will not be modified:

            >>> import pandas as pd
            >>> data = pd.DataFrame([{'a': 1, 'b': 2}, {'a': 3, 'b': 4}])
            >>> data
               a  b
            0  1  2
            1  3  4
            >>> filtered_data = data[pd.Series([True, False])]
            >>> filtered_data
               a  b
            0  1  2
            >>> filtered_data["a"][0] = 10
            >>> filtered_data
                a  b
            0  10  2
            >>> data
               a  b
            0  1  2
            1  3  4
        """
        return self.__data

    @data.setter
    def data(self, data: Union[pd.DataFrame, None]):
        """Data setter.

        Args:
            data (Union[pd.DataFrame, None]): data information. It must follow
                the structure defined by its columns, indices, required
                columns, and columns types. If None empty DataFrame is created.

        Raises:
            ValueError: if missing required column.
            TypeError: invalid column type.
        """
        if data is None:
            data = pd.DataFrame(columns=self._columns)

        data = self._validate_data(data)
        data = self.__sort_columns(data)
        if self._sort:
            data = self.__sort_rows(data)

        self.__data = data

    @property
    def data_idx(self) -> pd.DataFrame:
        """Data information indexed by defined indices.

        Returns:
            pd.DataFrame: indexed data information.

        Example:

            Without indices:

            >>> from optimization_autobots.domain.aggregation import Aggregation
            >>> import pandas as pd
            >>> aggregation = Aggregation()
            >>> aggregation._columns = ['index1', 'column1']
            >>> aggregation.data = pd.DataFrame([{'index1': 0, 'column1': 1}])
            >>> aggregation.data_idx
               index1  column1
            0       0        1

            With defined indices:

            >>> from optimization_autobots.domain.aggregation import Aggregation
            >>> import pandas as pd
            >>> aggregation = Aggregation()
            >>> aggregation._columns = ['index1', 'column1']
            >>> aggregation._indices = ['index1']
            >>> aggregation.data = pd.DataFrame([{'index1': 0, 'column1': 1}])
            >>> aggregation.data_idx # doctest: +NORMALIZE_WHITESPACE
                    column1
            index1
            0             1

            It doesn't modify the original data:

            >>> from optimization_autobots.domain.aggregation import Aggregation
            >>> import pandas as pd
            >>> aggregation = Aggregation()
            >>> aggregation._columns = ['index1', 'column1']
            >>> aggregation._indices = ['index1']
            >>> aggregation.data = pd.DataFrame([{'index1': 0, 'column1': 1}])
            >>> df = aggregation.data_idx
            >>> df # doctest: +NORMALIZE_WHITESPACE
                    column1
            index1
            0             1
            >>> df['column1'][0] = 10
            >>> df # doctest: +NORMALIZE_WHITESPACE
                    column1
            index1
            0            10
            >>> aggregation.data_idx # doctest: +NORMALIZE_WHITESPACE
                    column1
            index1
            0             1
            >>> aggregation.data
               index1  column1
            0       0        1
        """
        if len(self._indices) == 0:
            return self.data
        return self._data.set_index(self._indices)

    @property
    def index(self) -> pd.Index:
        """Indices of the aggregation.

        Returns:
            pd.Index: data index.

        Example:

            >>> from optimization_autobots.domain.aggregation import Aggregation
            >>> import pandas as pd
            >>> aggregation = Aggregation()
            >>> aggregation._columns = ['index1', 'column1']
            >>> aggregation._indices = ['index1']
            >>> aggregation.data = pd.DataFrame([{'index1': 0, 'column1': 1}])
            >>> aggregation.index
            Index([0], dtype='int64', name='index1')
        """
        return self.data_idx.index

    def _validate_data(self, data: Union[pd.DataFrame, None], add_missing_columns: bool = True) -> pd.DataFrame:
        """Validate data object.

        Args:
            data (Union[pd.DataFrame, None]): data object.
            add_missing_columns (bool, optional): if True add missing columns
                in the data object with its default value. Defaults to True.

        Raises:
            TypeError: if invalid data type.

        Returns:
            pd.DataFrame: data object.

        Example:

            Using default values:

            >>> from optimization_autobots.domain.aggregation import Aggregation
            >>> import pandas as pd
            >>> aggregation = Aggregation()
            >>> aggregation._columns = ['index1', 'column1']
            >>> aggregation._columns_type = {'index1': int, 'column1': int}
            >>> aggregation._default_column_values = {'column1': 1}
            >>> aggregation._validate_data(pd.DataFrame([{'index1': 0}]))
               index1  column1
            0       0        1

            Using add missing columns with False:

            >>> from optimization_autobots.domain.aggregation import Aggregation
            >>> import pandas as pd
            >>> aggregation = Aggregation()
            >>> aggregation._columns = ['index1', 'column1']
            >>> aggregation._columns_type = {'index1': int, 'column1': int}
            >>> aggregation._default_column_values = {'column1': 1}
            >>> aggregation._validate_data(
            ...     pd.DataFrame([{'index1': 0}]), add_missing_columns=False
            ... )
               index1
            0       0
        """
        if isinstance(data, pd.DataFrame):
            data = self.__validate_columns(data)
            if add_missing_columns:
                data = self.__add_missing_columns(data)
        else:
            raise TypeError(f"[{self.__class__.__name__}] " f"Invalid data type: {type(data).__name__}")

        data = self.__replace_nan_with_default_value(data)
        data = self.__validate_type(data)

        return data

    def __validate_columns(self, data: pd.DataFrame) -> pd.DataFrame:
        """Validate data columns.

        Args:
            data (pd.DataFrame): data object.

        Raises:
            ValueError: if missing required column.

        Returns:
            pd.DataFrame: data object.
        """
        # Check required columns
        columns = [c for c in self._columns if c in data.columns]
        missing_required_columns = [c for c in self._required_columns if c not in columns]
        if len(missing_required_columns) > 0:
            raise ValueError(
                f"[{self.__class__.__name__}] "
                f"Required columns not found: "
                f"{', '.join([str(e) for e in missing_required_columns])}"
            )

        # Warning with unknown columns
        unknown_columns = [c for c in data.columns if c not in self._columns]
        if len(unknown_columns) > 0:
            log.warning(
                f"[{self.__class__.__name__}] " f"Unknown columns: " f"{', '.join([str(e) for e in unknown_columns])}"
            )

        # Remove duplicated rows
        if len(self._indices) == 0:
            data = data.drop_duplicates(subset=columns, ignore_index=self._ignore_index)
        else:
            data = data.drop_duplicates(subset=self._indices, keep="last", ignore_index=self._ignore_index)

        return data

    def __sort_columns(self, data: pd.DataFrame) -> pd.DataFrame:
        """Sort columns of the aggregation object.

        Args:
            data (pd.DataFrame): data.

        Returns:
            pd.DataFrame: sorted data.
        """
        return data[self._columns]

    def __sort_rows(self, data: pd.DataFrame) -> pd.DataFrame:
        """Sort rows of the aggregation object.

        Args:
            data (pd.DataFrame): data.

        Returns:
            pd.DataFrame: sorted data.
        """
        data.sort_values(by=self._indices, ignore_index=self._ignore_index, inplace=True)
        return data

    def __add_missing_columns(self, data: pd.DataFrame) -> pd.DataFrame:
        """Add missing columns in the data object with its default value.

        Args:
            data (pd.DataFrame): data object.

        Returns:
            pd.DataFrame: data object.
        """
        # Update missing information with default values
        unknown_columns = [c for c in self._columns if c not in data.columns]
        for c in unknown_columns:
            log.warning(
                f"[{self.__class__.__name__}] "
                f"No information for column {c}. "
                f"Set default value: {self._default_column_values[c]}"
            )
            data[c] = self._default_column_values[c]

        return data

    def __replace_nan_with_default_value(self, data: pd.DataFrame) -> pd.DataFrame:
        """Replace nan with default value.

        Args:
            data (pd.DataFrame): data object.

        Returns:
            pd.DataFrame: data object.
        """
        default_values = {c: v for c, v in self._default_column_values.items() if c in data.columns}
        data = data.fillna(default_values)
        return data

    def __validate_type(self, data: pd.DataFrame) -> pd.DataFrame:
        """Validate data columns types.

        Args:
            data (pd.DataFrame): data object.

        Returns:
            pd.DataFrame: data object.
        """
        if len(self._columns_type) > 0:
            valid_types = {k: v for k, v in self._columns_type.items() if k in data.columns}
            for column, dtype in valid_types.items():
                if data[column].dtype != dtype:
                    data[column] = data[column].astype(dtype)

        return data

    def add(self, **kargs):
        """Add a new entry to the aggregation object.

        Args:
            **kargs: key-value (column name and its value) pairs of data to
                add.

        Examples:

            >>> from optimization_autobots.domain.aggregation import Aggregation
            >>> aggregation = Aggregation()
            >>> aggregation._columns = ['index1', 'column1']
            >>> aggregation
            Empty Aggregation

            We can add a new entry to the aggregation object:

            >>> aggregation.add(index1=0, column1=1)
            >>> aggregation
               index1  column1
            0       0        1

            Duplicated rows are removed:

            >>> aggregation.add(index1=0, column1=1)
            >>> aggregation
               index1  column1
            0       0        1

            If we set the index the behavior is similar, but last entry is
            considered:

            >>> from optimization_autobots.domain.aggregation import Aggregation
            >>> aggregation = Aggregation()
            >>> aggregation._columns = ['index1', 'column1']
            >>> aggregation._indices = ['index1']
            >>> aggregation.add(index1=0, column1=1)
            >>> aggregation
               index1  column1
            0       0        1
            >>> aggregation.add(index1=0, column1=2)
            >>> aggregation
               index1  column1
            0       0        2
        """
        new_data = pd.DataFrame([kargs])
        new_data = self._validate_data(new_data, add_missing_columns=True)

        self.data = pd.concat([self.data, new_data], ignore_index=self._ignore_index)

    def update(self, data: pd.DataFrame):
        """Update the data of the aggregation object. This method only works if
        indices are defined.

        Args:
            data (pd.DataFrame): data object to update the data aggregation
                object.

        Examples:
            If we don't define indices, the update method don't update the data:

            >>> from optimization_autobots.domain.aggregation import Aggregation
            >>> import pandas as pd
            >>> aggregation = Aggregation()
            >>> aggregation._columns = ['index1', 'column1', 'column2']
            >>> aggregation.add(index1=0, column1=1, column2=2)
            >>> aggregation
               index1  column1  column2
            0       0        1        2
            >>> aggregation.update(
            ...     data=pd.DataFrame([{'index1': 0, 'column1': 2, 'column2': 3}])
            ... )
            >>> aggregation
               index1  column1  column2
            0       0        1        2

            But if we define indices, the update method update the data taking
            the indices into consideration:

            >>> from optimization_autobots.domain.aggregation import Aggregation
            >>> import pandas as pd
            >>> aggregation = Aggregation()
            >>> aggregation._columns = ['index1', 'column1', 'column2']
            >>> aggregation._indices = ['index1']
            >>> aggregation.add(index1=0, column1=1, column2=2)
            >>> aggregation
               index1  column1  column2
            0       0        1        2
            >>> aggregation.update(
            ...     data=pd.DataFrame([{'index1': 0, 'column1': 2, 'column2': 3}])
            ... )
            >>> aggregation
               index1  column1  column2
            0       0        2        3

            Also, we can update the data of a subset of columns that aren't
            indices:

            >>> from optimization_autobots.domain.aggregation import Aggregation
            >>> import pandas as pd
            >>> aggregation = Aggregation()
            >>> aggregation._columns = ['index1', 'column1', 'column2']
            >>> aggregation._columns_type = {'column1': 'int', 'column2': 'int'}
            >>> aggregation._indices = ['index1']
            >>> aggregation.add(index1=0, column1=1, column2=2)
            >>> aggregation.add(index1=1, column1=2, column2=3)
            >>> aggregation
               index1  column1  column2
            0       0        1        2
            1       1        2        3
            >>> aggregation.update(data=pd.DataFrame([{'index1': 0, 'column2': 10}]))
            >>> aggregation
               index1  column1  column2
            0       0        1       10
            1       1        2        3

            If we update the data with a new index, nothing happens:

            >>> from optimization_autobots.domain.aggregation import Aggregation
            >>> import pandas as pd
            >>> aggregation = Aggregation()
            >>> aggregation._columns = ['index1', 'column1', 'column2']
            >>> aggregation._columns_type = {'column1': 'int', 'column2': 'int'}
            >>> aggregation._indices = ['index1']
            >>> aggregation.add(index1=0, column1=1, column2=2)
            >>> aggregation.add(index1=1, column1=2, column2=3)
            >>> aggregation
               index1  column1  column2
            0       0        1        2
            1       1        2        3
            >>> aggregation.update(data=pd.DataFrame([{'index1': 10, 'column2': 10}]))
            >>> aggregation
               index1  column1  column2
            0       0        1        2
            1       1        2        3

            If we update the data with a some existing and some new index, only existing ones are updated:

            >>> from optimization_autobots.domain.aggregation import Aggregation
            >>> import pandas as pd
            >>> aggregation = Aggregation()
            >>> aggregation._columns = ['index1', 'column1', 'column2']
            >>> aggregation._columns_type = {'column1': 'int', 'column2': 'int'}
            >>> aggregation._indices = ['index1']
            >>> aggregation.add(index1=0, column1=1, column2=2)
            >>> aggregation.add(index1=1, column1=2, column2=3)
            >>> aggregation
               index1  column1  column2
            0       0        1        2
            1       1        2        3
            >>> aggregation.update(data=pd.DataFrame([{'index1': 0, 'column2': 10}, {'index1': 10, 'column2': 10}]))
            >>> aggregation
               index1  column1  column2
            0       0        1       10
            1       1        2        3

            Update multiple columns:

            >>> from optimization_autobots.domain.aggregation import Aggregation
            >>> import pandas as pd
            >>> aggregation = Aggregation()
            >>> aggregation._columns = ['index1', 'column1', 'column2']
            >>> aggregation._columns_type = {'column1': 'int', 'column2': 'int'}
            >>> aggregation._indices = ['index1']
            >>> aggregation.add(index1=0, column1=1, column2=2)
            >>> aggregation.add(index1=1, column1=2, column2=3)
            >>> aggregation
               index1  column1  column2
            0       0        1        2
            1       1        2        3
            >>> aggregation.update(data=pd.DataFrame([
            ...     {'index1': 1, 'column1': 30, 'column2': 40},
            ...     {'index1': 0, 'column1': 10, 'column2': 20},
            ... ]))
            >>> aggregation
               index1  column1  column2
            0       0       10       20
            1       1       30       40

            Not update NA values:

            >>> from optimization_autobots.domain.aggregation import Aggregation
            >>> import pandas as pd
            >>> aggregation = Aggregation()
            >>> aggregation._columns = ['index1', 'column1', 'column2']
            >>> aggregation._columns_type = {'column1': "Int32", 'column2': "Int32"}
            >>> aggregation._indices = ['index1']
            >>> aggregation.add(index1=0, column1=1, column2=2)
            >>> aggregation.add(index1=1, column1=2, column2=3)
            >>> aggregation
               index1  column1  column2
            0       0        1        2
            1       1        2        3
            >>> aggregation.update(data=pd.DataFrame([
            ...     {'index1': 1, 'column1': 30, 'column2': pd.NA},
            ...     {'index1': 0, 'column1': pd.NA, 'column2': 20},
            ... ]))
            >>> aggregation
               index1  column1  column2
            0       0        1       20
            1       1       30        3
        """
        if len(self._indices) == 0:
            log.warning("There are no indices to update the data")
        else:
            data = self._validate_data(data, add_missing_columns=False)
            current_data_idx = self._data.set_index(self._indices)
            new_data_idx = data.set_index(self._indices)

            columns_to_update = list(set(new_data_idx.columns.values.tolist()).intersection(set(self._columns)))

            for column in columns_to_update:
                valid_indices = new_data_idx[new_data_idx[column].notna()].index
                indices_to_update = current_data_idx.index.intersection(valid_indices)
                if len(indices_to_update) > 0:
                    current_data_idx.loc[indices_to_update, column] = new_data_idx.loc[indices_to_update, column].values

            self.data = current_data_idx.reset_index()

    def merge(self, *aggregations: Aggregation) -> pd.DataFrame:
        """Merge the data of different aggregation objects taking into
        consideration the indices of the current object.

        Args:
            *aggregations (Aggregation): aggregation objects we want to merge.

        Returns:
            pd.DataFrame: merged data.

        Examples:
            >>> from optimization_autobots.domain.aggregation import Aggregation
            >>> aggregation1 = Aggregation()
            >>> aggregation1._columns = ['index1', 'column1']
            >>> aggregation1._indices = ['index1']
            >>> aggregation1.add(index1=0, column1=1)
            >>> aggregation1.add(index1=1, column1=10)
            >>> aggregation1
               index1  column1
            0       0        1
            1       1       10
            >>> aggregation2 = Aggregation()
            >>> aggregation2._columns = ['index1', 'index2', 'column2']
            >>> aggregation2._indices = ['index1', 'index2']
            >>> aggregation2.add(index1=0, index2=0, column2=2)
            >>> aggregation2.add(index1=0, index2=1, column2=3)
            >>> aggregation2.add(index1=1, index2=0, column2=4)
            >>> aggregation2.add(index1=1, index2=1, column2=5)
            >>> aggregation2
               index1  index2  column2
            0       0       0        2
            1       0       1        3
            2       1       0        4
            3       1       1        5
            >>> merged_df = aggregation2.merge(aggregation1)
            >>> merged_df
               index1  index2  column2  column1
            0       0       0        2        1
            1       0       1        3        1
            2       1       0        4       10
            3       1       1        5       10

            If we change any value of the df involved in the merge, the merge data does not change.

            >>> aggregation2.update(
            ...     data=pd.DataFrame([{'index1': 0, 'index2': 0, 'column2': 100}])
            ... )
            >>> aggregation2
               index1  index2  column2
            0       0       0      100
            1       0       1        3
            2       1       0        4
            3       1       1        5
            >>> merged_df
               index1  index2  column2  column1
            0       0       0        2        1
            1       0       1        3        1
            2       1       0        4       10
            3       1       1        5       10
        """
        data = self.data
        for aggregation in aggregations:
            if isinstance(aggregation, Aggregation):
                common_idx = list(set(self._indices).intersection(aggregation._indices))
                if len(common_idx) > 0:
                    data = pd.merge(data, aggregation.data, how="left", on=common_idx)
                else:
                    log.warning(
                        f"No common idx between '{self.__class__.__name__}' "
                        f"and '{aggregation.__class__.__name__}' aggregation"
                    )
            else:
                log.warning(f"{aggregation.__class__.__name__} is not a subclass of " "Aggregation")
        return data

    def copy(self):
        """Copy the aggregation object.

        Examples:
            >>> from optimization_autobots.domain.aggregation import Aggregation
            >>> class AggregationExample(Aggregation):
            ...     _columns = ['index1', 'column1']
            ...     _indices = ['index1']
            >>> aggregation = AggregationExample()
            >>> aggregation.add(index1=0, column1=1)
            >>> aggregation.add(index1=1, column1=10)
            >>> aggregation
              index1 column1
            0      0       1
            1      1      10
            >>> aggregation_copy = aggregation.copy()
            >>> aggregation_copy
              index1 column1
            0      0       1
            1      1      10
            >>> aggregation_copy.add(index1=2, column1=100)
            >>> aggregation_copy
              index1 column1
            0      0       1
            1      1      10
            2      2     100
            >>> aggregation
              index1 column1
            0      0       1
            1      1      10
        """
        return self.__class__(data=self.data)

    def to_string(self) -> str:
        """String representation of the dataframe

        Returns:
            str: string representation of the dataframe.

        Examples:
            >>> from optimization_autobots.domain.aggregation import Aggregation
            >>> import pandas as pd
            >>> aggregation = Aggregation()
            >>> aggregation._columns = ['index1', 'column1']
            >>> aggregation.to_string()
            'Empty Aggregation'
            >>> aggregation.data = pd.DataFrame([{'index1': 0, 'column1': 1}])
            >>> aggregation.to_string()
            '   index1  column1\\n0       0        1'
        """
        if len(self) > 0:
            representation = self._data.to_string()
        else:
            representation = f"Empty {self.__class__.__name__}"
        return representation

    def pprint(self):
        """Pretty print.

        It prints the data in a pretty format by using to_string method.

        Examples:
            >>> from optimization_autobots.domain.aggregation import Aggregation
            >>> import pandas as pd
            >>> aggregation = Aggregation()
            >>> aggregation._columns = ['index1', 'column1']
            >>> aggregation.data = pd.DataFrame([{'index1': 0, 'column1': 1}])
            >>> aggregation.pprint()
               index1  column1
            0       0        1
        """
        return print(self.to_string())

    def __len__(self) -> int:
        """Number of rows of the data.

        Returns:
            int: number of rows of the data.

        Examples:
            >>> from optimization_autobots.domain.aggregation import Aggregation
            >>> aggregation = Aggregation()
            >>> len(aggregation)
            0
        """
        return self._data.shape[0]

    def __getitem__(self, column: str | list) -> pd.Series | pd.DataFrame:
        """Get the data of a column.

        Args:
            column (str | list): name or list of names of the column to get.

        Returns:
            pd.Series | pd.DataFrame: data of the column or dataframe with the columns information.

        Examples:
            >>> from optimization_autobots.domain.aggregation import Aggregation
            >>> aggregation = Aggregation()
            >>> aggregation._columns = ['index1', 'column1']
            >>> aggregation._indices = ['index1']
            >>> aggregation.add(index1=0, column1=1)
            >>> aggregation.add(index1=1, column1=10)
            >>> aggregation['column1']
            0     1
            1    10
            Name: column1, dtype: int64

            If a value of a aggregation copy changes the original does not change.

            >>> df = aggregation['column1']
            >>> df.loc[0] = 5
            >>> df
            0     5
            1    10
            Name: column1, dtype: int64
            >>> aggregation['column1']
            0     1
            1    10
            Name: column1, dtype: int64
        """
        return self.data[column]

    def __repr__(self) -> str:
        """Representation of the object.

        Returns:
            str: representation of the object.

        Examples:
            >>> from optimization_autobots.domain.aggregation import Aggregation
            >>> aggregation = Aggregation()
            >>> aggregation._columns = ['index1', 'column1']
            >>> aggregation._indices = ['index1']
            >>> aggregation.add(index1=0, column1=1)
            >>> aggregation.add(index1=1, column1=10)
            >>> aggregation
               index1  column1
            0       0        1
            1       1       10
        """
        if len(self) > 0:
            representation = self.data.__repr__()
        else:
            representation = f"Empty {self.__class__.__name__}"

        return representation

    def _repr_html_(self) -> str:
        """HTML representation of the object.

        Returns:
            str: HTML representation of the object.
        """
        return self._data._repr_html_()  # type: ignore
