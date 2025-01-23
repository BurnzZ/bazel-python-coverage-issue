## Overview

`bazel coverage` fails without any useful messages when some Python packages are
being used/imported. Some examples:

- `torchvision`
- `transformers.models.distilbert.DistilBertModel`

## To reproduce the issue

Uncomment any of these lines in `test.py`:
```python
import torchvision
from transformers.models.distilbert import DistilBertModel
```

Then run the following in an attempt to get the coverage:

```bash
bazel coverage --combined_report=lcov :test --nocache_test_results --test_output=all

lcov --list "$(bazel info output_path)/_coverage/_coverage_report.dat"
```

This would lead to this output which fails without any context ❌:

```bash
$ bazel coverage --combined_report=lcov :test --nocache_test_results --test_output=all

INFO: Using default value for --instrumentation_filter: "^//".
INFO: Override the above default with --instrumentation_filter
INFO: Analyzed target //:test (0 packages loaded, 0 targets configured).
FAIL: //:test (Exit 1) (see /private/var/tmp/_bazel_user/c97d0f59e3791eddf9709b879355cbf5/execroot/_main/bazel-out/darwin_arm64-fastbuild/testlogs/test/test.log)
INFO: From Testing //:test:
==================== Test output for //:test:
--
Coverage runner: Not collecting coverage for failed test.
The following commands failed with status 1
/private/var/tmp/_bazel_user/c97d0f59e3791eddf9709b879355cbf5/sandbox/darwin-sandbox/7/execroot/_main/bazel-out/darwin_arm64-fastbuild/bin/test.runfiles/_main/test
================================================================================
INFO: LCOV coverage report is located at /private/var/tmp/_bazel_user/c97d0f59e3791eddf9709b879355cbf5/execroot/_main/bazel-out/_coverage/_coverage_report.dat
 and execpath is bazel-out/_coverage/_coverage_report.dat
INFO: From Coverage report generation:
Jan. 23, 2025 4:55:51 PM com.google.devtools.coverageoutputgenerator.Main getTracefiles
INFO: Found 1 tracefiles.
Jan. 23, 2025 4:55:51 PM com.google.devtools.coverageoutputgenerator.Main parseFilesSequentially
INFO: Parsing file bazel-out/darwin_arm64-fastbuild/testlogs/test/coverage.dat
Jan. 23, 2025 4:55:51 PM com.google.devtools.coverageoutputgenerator.Main getGcovInfoFiles
INFO: No gcov info file found.
Jan. 23, 2025 4:55:51 PM com.google.devtools.coverageoutputgenerator.Main getGcovJsonInfoFiles
INFO: No gcov json file found.
Jan. 23, 2025 4:55:51 PM com.google.devtools.coverageoutputgenerator.Main getProfdataFileOrNull
INFO: No .profdata file found.
Jan. 23, 2025 4:55:51 PM com.google.devtools.coverageoutputgenerator.Main runWithArgs
WARNING: There was no coverage found.
INFO: Found 1 test target...
Target //:test up-to-date:
  bazel-bin/test
INFO: Elapsed time: 14.578s, Critical Path: 14.22s
INFO: 3 processes: 2 action cache hit, 3 darwin-sandbox.
INFO: Build completed, 1 test FAILED, 3 total actions
//:test                                                                  FAILED in 13.7s
  /private/var/tmp/_bazel_user/c97d0f59e3791eddf9709b879355cbf5/execroot/_main/bazel-out/darwin_arm64-fastbuild/testlogs/test/test.log

Executed 1 out of 1 test: 1 fails locally.
```

```bash
$ lcov --list "$(bazel info output_path)/_coverage/_coverage_report.dat"

lcov: ERROR: (empty) no valid records found in tracefile /private/var/tmp/_bazel_user/c97d0f59e3791eddf9709b879355cbf5/execroot/_main/bazel-out/_coverage/_coverage_report.dat
        (use "lcov --ignore-errors empty ..." to bypass this error)
```

Note that when `bazel test` is used, the code runs successfully:

```bash
$ bazel test :test --nocache_test_results --test_output=all

INFO: Analyzed target //:test (0 packages loaded, 0 targets configured).
INFO: From Testing //:test:
==================== Test output for //:test:
================================================================================
INFO: Found 1 test target...
Target //:test up-to-date:
  bazel-bin/test
INFO: Elapsed time: 4.165s, Critical Path: 4.03s
INFO: 2 processes: 2 darwin-sandbox.
INFO: Build completed successfully, 2 total actions
//:test                                                                  PASSED in 3.7s

Executed 1 out of 1 test: 1 test passes.
There were tests whose specified size is too big. Use the --test_verbose_timeout_warnings command line option to see which ones these are.
```


However, commenting those imports above should lead to a successful test coverage ✅:

```bash
$ bazel coverage --combined_report=lcov :test --nocache_test_results --test_output=all

Starting local Bazel server (8.0.1) and connecting to it...
INFO: Using default value for --instrumentation_filter: "^//".
INFO: Override the above default with --instrumentation_filter
INFO: Analyzed target //:test (132 packages loaded, 20860 targets configured).
INFO: From Testing //:test:
==================== Test output for //:test:
GCov does not exist at the given path: ''
Jan. 23, 2025 5:53:48 AM com.google.devtools.coverageoutputgenerator.Main getTracefiles
INFO: Found 1 tracefiles.
Jan. 23, 2025 5:53:48 AM com.google.devtools.coverageoutputgenerator.Main parseFilesSequentially
INFO: Parsing file /private/var/tmp/_bazel_user/c97d0f59e3791eddf9709b879355cbf5/sandbox/darwin-sandbox/4/execroot/_main/bazel-out/darwin_arm64-fastbuild/testlogs/_coverage/test/test/pylcov.dat
Jan. 23, 2025 5:53:48 AM com.google.devtools.coverageoutputgenerator.Main getGcovInfoFiles
INFO: No gcov info file found.
Jan. 23, 2025 5:53:48 AM com.google.devtools.coverageoutputgenerator.Main getGcovJsonInfoFiles
INFO: No gcov json file found.
Jan. 23, 2025 5:53:48 AM com.google.devtools.coverageoutputgenerator.Main getProfdataFileOrNull
INFO: No .profdata file found.
================================================================================
INFO: LCOV coverage report is located at /private/var/tmp/_bazel_user/c97d0f59e3791eddf9709b879355cbf5/execroot/_main/bazel-out/_coverage/_coverage_report.dat
 and execpath is bazel-out/_coverage/_coverage_report.dat
INFO: From Coverage report generation:
Jan. 23, 2025 4:53:48 PM com.google.devtools.coverageoutputgenerator.Main getTracefiles
INFO: Found 1 tracefiles.
Jan. 23, 2025 4:53:48 PM com.google.devtools.coverageoutputgenerator.Main parseFilesSequentially
INFO: Parsing file bazel-out/darwin_arm64-fastbuild/testlogs/test/coverage.dat
Jan. 23, 2025 4:53:48 PM com.google.devtools.coverageoutputgenerator.Main getGcovInfoFiles
INFO: No gcov info file found.
Jan. 23, 2025 4:53:48 PM com.google.devtools.coverageoutputgenerator.Main getGcovJsonInfoFiles
INFO: No gcov json file found.
Jan. 23, 2025 4:53:48 PM com.google.devtools.coverageoutputgenerator.Main getProfdataFileOrNull
INFO: No .profdata file found.
INFO: Found 1 test target...
Target //:test up-to-date:
  bazel-bin/test
INFO: Elapsed time: 29.115s, Critical Path: 6.96s
INFO: 18 processes: 12 internal, 5 darwin-sandbox, 1 worker.
INFO: Build completed successfully, 18 total actions
//:test                                                                  PASSED in 1.6s
  /private/var/tmp/_bazel_user/c97d0f59e3791eddf9709b879355cbf5/execroot/_main/bazel-out/darwin_arm64-fastbuild/testlogs/test/coverage.dat

Executed 1 out of 1 test: 1 test passes.
There were tests whose specified size is too big. Use the --test_verbose_timeout_warnings command line option to see which ones these are.
```

```bash
$ lcov --list "$(bazel info output_path)/_coverage/_coverage_report.dat"

            |Lines       |Functions
Filename    |Rate     Num|Rate    Num
=====================================
[/]
main.py     |50.0%      2|    -     0
=====================================
      Total:|50.0%      2|    -     0
Message summary:
  no messages were reported
```
