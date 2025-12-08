# Updating Test 008 Reference Data

The easiest way to update the reference data for test 008 (`008_reference`) is the following:

```
cd $GEMSHOME/tests
export GEMS_KEEP_BAD_OUTPUTS=True
./run_tests.sh 008.test.multi-conformer-builds.sh
mv correct_outputs/008_reference correct_outputs/008_reference_bak_git-ignore-me
mv bad_outputs/YYYY-MM-DD-HH-MM/ correct_outputs/008_reference
rm -rf bad_outputs
unset GEMS_KEEP_BAD_OUTPUTS
```

Replace YYYY-MM-DD-HH-MM with the date-time appropriate to your current date-time.

If you are happy, then also remove `correct_outputs/008_reference_bak_git-ignore-me`.

Commit the changes.
