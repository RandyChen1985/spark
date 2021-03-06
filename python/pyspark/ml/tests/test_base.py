#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import unittest

from pyspark.sql.types import DoubleType, IntegerType
from pyspark.testing.mlutils import MockDataset, MockEstimator, MockUnaryTransformer, \
    SparkSessionTestCase


class UnaryTransformerTests(SparkSessionTestCase):

    def test_unary_transformer_validate_input_type(self):
        shiftVal = 3
        transformer = MockUnaryTransformer(shiftVal=shiftVal) \
            .setInputCol("input").setOutputCol("output")

        # should not raise any errors
        transformer.validateInputType(DoubleType())

        with self.assertRaises(TypeError):
            # passing the wrong input type should raise an error
            transformer.validateInputType(IntegerType())

    def test_unary_transformer_transform(self):
        shiftVal = 3
        transformer = MockUnaryTransformer(shiftVal=shiftVal) \
            .setInputCol("input").setOutputCol("output")

        df = self.spark.range(0, 10).toDF('input')
        df = df.withColumn("input", df.input.cast(dataType="double"))

        transformed_df = transformer.transform(df)
        results = transformed_df.select("input", "output").collect()

        for res in results:
            self.assertEqual(res.input + shiftVal, res.output)


class EstimatorTest(unittest.TestCase):

    def testDefaultFitMultiple(self):
        N = 4
        data = MockDataset()
        estimator = MockEstimator()
        params = [{estimator.fake: i} for i in range(N)]
        modelIter = estimator.fitMultiple(data, params)
        indexList = []
        for index, model in modelIter:
            self.assertEqual(model.getFake(), index)
            indexList.append(index)
        self.assertEqual(sorted(indexList), list(range(N)))


if __name__ == "__main__":
    from pyspark.ml.tests.test_base import *

    try:
        import xmlrunner
        testRunner = xmlrunner.XMLTestRunner(output='target/test-reports')
    except ImportError:
        testRunner = None
    unittest.main(testRunner=testRunner, verbosity=2)
