"""
**Events**

- 2023-04-15 [2.0.0] add docker file and image
- 2021-12-09 [1.5.0] add random factor to review datetime
- 2021-11-14 [1.4.0] add practice list function
- 2021-09-17 [1.3.0] update settings show paraphrase
- 2021-04-30 [1.2.1] update settings
- 2021-03-03 [1.2.0] adjust review strategy
- 2020-05-07 [1.1.3] fix bug for django version
- 2020-05-07 [1.1.2] add resources
- 2020-02-26 [1.1.1] fix bug for resources
- 2019-07-06 [1.1.0] add youdao and baidu url in word card
- 2019-04-04 [1.0.0] update for performance
- 2019-03-08 [0.21.2] fix bug for updater
- 2019-03-08 [0.21.1] update semantic version to 2.4
- 2018-12-26 [0.21.0] update download method
- 2018-06-13 [0.20.4] refine resource list
- 2018-06-11 [0.20.3] refine resource list
- 2018-06-10 [0.20.2] fix bug for resource list
- 2018-05-06 [0.20.1] fix bug for practice
- 2018-04-25 [0.20.0] add date count in date menu
- 2018-04-21 [0.19.1] fix bug for starter duplicate start server
- 2018-04-21 [0.19.0] translate resource name
- 2018-04-21 [0.18.6] test for updater
- 2018-04-21 [0.18.5] test for updater
- 2018-04-21 [0.18.4] test for updater
- 2018-04-21 [0.18.3] test for updater
- 2018-04-21 [0.18.2] test for updater
- 2018-04-21 [0.18.1] test for updater
- 2018-04-21 [0.18.0] redesign homepage
- 2018-04-21 [0.17.0] improve updater (no publish)
- 2018-04-12 [0.16.1] fix bug for url reverse error in found
- 2018-04-07 [0.16.0] add setting for alert dialog and help page in menu
- 2018-04-01 [0.15.2] fix bug for practice mode
- 2018-03-31 [0.15.1] fix bug for reset review
- 2018-03-31 [0.15.0] add reset review edit menu and dialog for danger operation
- 2018-02-10 [0.14.1] fix several bug
- 2018-02-08 [0.14.0] open resource in new tab
- 2018-02-08 [0.13.2] downgrade semantic ui to 2.2.13, cause of 2.2.14 critical bug of dropdown
- 2018-02-08 [0.13.1] improve experience for remove google fonts in semantic ui
- 2018-02-07 [0.13.0] add setting for study mode
- 2018-02-07 [0.12.4] fix bug for update progress
- 2018-02-07 [0.12.3] fix bug for migrations
- 2018-02-06 [0.12.2] update semantic ui to version 2.2.14
- 2018-02-06 [0.12.1] fix bug for show word card and add message in updater
- 2018-02-06 [0.12.0] add 'Show word card' in resource list
- 2018-02-06 [0.11.0] add 'Add to Review' button in resource list
- 2018-02-02 [0.10.1] refine resources
- 2018-02-02 [0.10.0] add count in date statistics
- 2018-02-02 [0.9.4] fix bug for youdao paraphrase
- 2018-01-13 [0.9.3] add target _blank to edit word
- 2018-01-06 [0.9.2] fix bug for study in checking
- 2018-01-02 [0.9.1] fix bug for youdao paraphrase
- 2018-01-02 [0.9.0] update footer information
- 2017-12-31 [0.8.4] fix bug for youdao paraphrase
- 2017-12-29 [0.8.3] fix bug for review skip count
- 2017-12-29 [0.8.2] fix bug
- 2017-12-29 [0.8.1] fix bug for version in update settings
- 2017-12-24 [0.8.0] add review paraphrase mode random with dictation
- 2017-12-19 [0.7.12] redesign next word and review hard word first
- 2017-12-19 [0.7.11] refine resources
- 2017-12-19 [0.7.10] remove study warning toast
- 2017-12-19 [0.7.9] fix bug for create time
- 2017-12-18 [0.7.8] fix bug for python2 non ascii
- 2017-12-18 [0.7.7] fix bug for study when system time changed in the schedule
- 2017-12-17 [0.7.6] fix bug for study
- 2017-12-17 [0.7.5] fix bug for study
- 2017-12-17 [0.7.4] fix bug for starter and study
- 2017-12-17 [0.7.3] fix bug for starter and study
- 2017-12-17 [0.7.2] fix bug for starter logger
- 2017-12-17 [0.7.1] fix bug for study when error
- 2017-12-17 [0.7.0] add label for phonetic download progress
- 2017-12-17 [0.6.1] redesign resource bar
- 2017-12-17 [0.6.0] refine resources
- 2017-12-17 [0.5.18] refine resources
- 2017-12-16 [0.5.17] fix bug for study bar, support python2
- 2017-12-16 [0.5.16] fix bug for found
- 2017-12-16 [0.5.15] fix bug for starter improve requirements.txt
- 2017-12-16 [0.5.14] fix bug for starter add migrate information
- 2017-12-16 [0.5.13] fix bug for starter add stop information
- 2017-12-16 [0.5.12] fix bug for starter add starter.log
- 2017-12-16 [0.5.11] add word type information in word card fooder
- 2017-12-15 [0.5.10] fix bug for study inexact equal word input
- 2017-12-14 [0.5.9] redesign count template
- 2017-12-14 [0.5.8] add review filter in resource list
- 2017-12-14 [0.5.7] fix bug for user and word unique in review and add index for word.title
- 2017-12-14 [0.5.6] fix bug for resource list
- 2017-12-13 [0.5.5] refine resources
- 2017-12-13 [0.5.4] refine resources
- 2017-12-12 [0.5.3] fix bug for update status log and refine resources
- 2017-12-12 [0.5.2] fix bug for update javascript
- 2017-12-12 [0.5.1] fix bug for update javascript
- 2017-12-12 [0.5.0] add filter in resource
- 2017-12-12 [0.4.2] fix bug for update
- 2017-12-12 [0.4.1] add update information and fix bug for django 2.0 many to many set
- 2017-12-11 [0.4.0] add starter.py instead of start.cmd and more intelligence
- 2017-12-01 [0.3.1] fix bug for update
- 2017-12-01 [0.3.0] add update function in settings
- 2017-11-30 [0.2.0] release first version for words
- 2017-11-26 [0.1.0] add many to project
- 2017-11-18 [0.0.1] finish utils youdao
"""

__version__ = ".".join(
    [str(var) for var in
        [
        2,
        0,
        0,
    ]
    ])

default_app_config = 'words.apps.Config'
