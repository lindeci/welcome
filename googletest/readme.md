
- [实践](#实践)
- [命令介绍](#命令介绍)
- [测试用例编写](#测试用例编写)
- [TEST\_F](#test_f)
- [BENCHMARK](#benchmark)
  - [例子](#例子)

# 实践
```bash
# 编译
 /usr/bin/cmake --build /data/mysql-server-8.2.0/build --config Debug --target hypergraph_optimizer-t -j 6
# 查看测试用例
./hypergraph_optimizer-t --gtest_list_tests
# 测试 其中 HypergraphOptimizerTest 是测试套件名称，SargableHyperpredicate 是测试用例名称
/data/mysql-server-8.2.0/build/runtime_output_directory/hypergraph_optimizer-t --gtest_filter=HypergraphOptimizerTest.SargableHyperpredicate
```

# 命令介绍
```bash
./hypergraph_optimizer-t --help
This program contains tests written using Google Test. You can use the
following command line flags to control its behavior:

Test Selection:
  --gtest_list_tests
      List the names of all tests instead of running them. The name of
      TEST(Foo, Bar) is "Foo.Bar".
  --gtest_filter=POSITIVE_PATTERNS[-NEGATIVE_PATTERNS]
      Run only the tests whose name matches one of the positive patterns but
      none of the negative patterns. '?' matches any single character; '*'
      matches any substring; ':' separates two patterns.
  --gtest_also_run_disabled_tests
      Run all disabled tests too.

Test Execution:
  --gtest_repeat=[COUNT]
      Run the tests repeatedly; use a negative count to repeat forever.
  --gtest_shuffle
      Randomize tests' orders on every iteration.
  --gtest_random_seed=[NUMBER]
      Random number seed to use for shuffling test orders (between 1 and
      99999, or 0 to use a seed based on the current time).
  --gtest_recreate_environments_when_repeating
      Sets up and tears down the global test environment on each repeat
      of the test.

Test Output:
  --gtest_color=(yes|no|auto)
      Enable/disable colored output. The default is auto.
  --gtest_brief=1
      Only print test failures.
  --gtest_print_time=0
      Don't print the elapsed time of each test.
  --gtest_output=(json|xml)[:DIRECTORY_PATH/|:FILE_PATH]
      Generate a JSON or XML report in the given directory or with the given
      file name. FILE_PATH defaults to test_detail.xml.
  --gtest_stream_result_to=HOST:PORT
      Stream test results to the given server.

Assertion Behavior:
  --gtest_death_test_style=(fast|threadsafe)
      Set the default death test style.
  --gtest_break_on_failure
      Turn assertion failures into debugger break-points.
  --gtest_throw_on_failure
      Turn assertion failures into C++ exceptions for use by an external
      test framework.
  --gtest_catch_exceptions=0
      Do not report exceptions as test failures. Instead, allow them
      to crash the program or throw a pop-up (on Windows).

Except for --gtest_list_tests, you can alternatively set the corresponding
environment variable of a flag (all letters in upper-case). For example, to
disable colored text output, you can either specify --gtest_color=no or set
the GTEST_COLOR environment variable to no.

For more information, please read the Google Test documentation at
https://github.com/google/googletest/. If you find a bug in Google Test
(not one in your own code or tests), please report it to
<googletestframework@googlegroups.com>.
```

# 测试用例编写
常用的宏
```cpp
TEST_F：这是一个宏，用于定义一个测试用例。TEST_F 需要两个参数：一个是测试套件名，另一个是测试用例名。

ASSERT_EQ：这是一个断言宏，用于检查两个值是否相等。如果不相等，ASSERT_EQ 会立即终止当前的测试函数。

EXPECT_EQ：这也是一个断言宏，用于检查两个值是否相等。但与 ASSERT_EQ 不同，即使检查失败，EXPECT_EQ 也不会终止当前的测试函数，而是允许测试继续进行。

SCOPED_TRACE：这是一个宏，用于在测试失败时提供有用的信息。SCOPED_TRACE 接受一个消息作为参数，如果在 SCOPED_TRACE 的作用域内的任何 Google Test 断言失败，这个消息就会被打印出来。

```
其它
```cpp
1. `TEST`：定义一个测试用例。`TEST` 需要两个参数：一个是测试套件名，另一个是测试用例名。

2. `TEST_F`：定义一个使用了测试夹具（fixture）的测试用例。`TEST_F` 需要两个参数：一个是测试夹具类的名字，另一个是测试用例名。

3. `ASSERT_*`：这是一类断言宏，用于检查条件是否为真。如果条件为假，`ASSERT_*` 会立即终止当前的测试函数。

4. `EXPECT_*`：这也是一类断言宏，用于检查条件是否为真。但与 `ASSERT_*` 不同，即使条件为假，`EXPECT_*` 也不会终止当前的测试函数，而是允许测试继续进行。

5. `SetUp`：这是一个在每个测试用例开始前都会被调用的函数，通常在测试夹具类中定义。你可以在 `SetUp` 函数中进行一些测试准备工作。

6. `TearDown`：这是一个在每个测试用例结束后都会被调用的函数，通常在测试夹具类中定义。你可以在 `TearDown` 函数中进行一些清理工作。

7. `SetUpTestCase` 和 `TearDownTestCase`：这两个函数在测试套件开始前和结束后分别被调用一次，通常在测试夹具类中定义。你可以在这两个函数中进行一些只需要进行一次的设置和清理工作。

8. `SCOPED_TRACE`：这是一个宏，用于在测试失败时提供有用的信息。`SCOPED_TRACE` 接受一个消息作为参数，如果在 `SCOPED_TRACE` 的作用域内的任何 Google Test 断言失败，这个消息就会被打印出来。

9. `RUN_ALL_TESTS`：这是一个宏，用于运行所有的测试用例。通常在 `main` 函数中调用。

10. `SUCCEED`：这是一个宏，用于表示一个测试用例成功。通常在你没有任何需要检查的条件，但又想表示测试成功时使用。
```

# TEST_F
TEST_F 的第一个参数TestFixtureName是个类，需要继承testing::Test，同时根据需要实现以下两个虚函数：
- virtual void SetUp()：在TEST_F中测试案例之前运行；
- virtual void TearDown()：在TEST_F之后运行。

可以类比对象的构造函数和析构函数。这样，同一个TestFixtureName下的每个TEST_F都会先执行SetUp，最后执行TearDwom。

此外，testing::Test还提供了两个static函数：
- static void SetUpTestSuite()：在第一个TEST之前运行
- static void TearDownTestSuite()：在最后一个TEST之后运行

# BENCHMARK

Google Benchmark 是一个用于对 C++ 代码进行基准测试的库，它提供了一些用于控制计时的函数，包括 `BENCHMARK`。当你想要在基准测试中排除某些代码的执行时间时，你可以使用 `BENCHMARK` 来定义一个基准测试。

以下是一些关于 `BENCHMARK` 的基本用法：

1. **定义基准测试**：你可以使用 `BENCHMARK` 宏来定义一个基准测试。例如，`BENCHMARK(BM_StringCreation);` 定义了一个名为 `BM_StringCreation` 的基准测试。

2. **设置基准测试参数**：你可以使用 `->Arg(arg)` 来为基准测试设置一个参数，或者使用 `->Range(start, end)` 来为基准测试设置一系列的参数。

3. **运行基准测试**：你可以使用 `BENCHMARK_MAIN();` 宏来定义一个 `main` 函数，这个函数会运行所有的基准测试。
## 例子
```cpp
StartBenchmarkTiming();
......
StopBenchmarkTiming();
```
可能输出结果：
```json
{
  "benchmarks": [
    {
      "name": "BM_SomeFunction",
      "iterations": 94877,
      "real_time": 29275,
      "cpu_time": 29836
    }
  ]
}
```