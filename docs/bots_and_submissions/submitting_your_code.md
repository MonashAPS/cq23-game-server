# Submitting Your Code

Once you're done with your code and want to submit it for the competition/leaderboards, you will need to upload a Zip archive on the
submissions page at https://teams.codequest.club. The archive should have your code's `Dockerfile` in its root. For
convenience, you can use this command to create your submission file. Open the terminal and go to your code's folder.
Then run:

```shell
cq23 zip
```

This will create a file called `submission.zip` in the same folder. You can then upload that file in teams portal.

Your submission will show "Pending" initially. Refresh the page after a few seconds, it will either show "Successful" or
"Failed". If your submission fails, there is something wrong with it and it won't be used for the competition.
Generally, if you run `cq23 run` on your computer and it works, then the submission will be fine. If not, the submission
will fail.