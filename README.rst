ASI toy calculator
==================

Description
-----------

This is a toy calculator using only additions and substractions (no `/`, `%` nor `*` operations used) to do "inifinite" calculations (meaning there is no overflow errors).

Usage
-----

- Run the client : `py client`

Inside the client there are multiple commands such as `help` which list the possibilities.

As per the main functionnality, it's simple maths. Here an example of possible calculation with different compatible symbols used :

`((3 - 2)! - 1 × √4 ÷ 2) + 20 - 20 × 3**3`

This is equivalent (and is internally converted) to :

`((3 - 2)! - 1 * V4 / 2) + 20 - 20 * 3 ^ 3`

 - Run tests : `py tests`
 - Calculate pi : `py calc_pi`

You may need to use another alias instead of `py` for calling python, such as `python` or `python3`, it depends on your env.
I did not make this a module nor did I added a shebang for linux compatibility, a matter of taste and compatibility.

Bonus context
-------------
I needed to level up my python knowledge. So I tried to redo a project from my CS school.

Some history of this project.

Base version made in like 4-5 days (6-8 hours), around 40h real time maybe. At first I thought I'd stop there.
I added a good week of work to handle float properly, debug some cases, double the number of tests and remove `floor()`, `/`, `%` and `*`. At that point there was maybe about 80h of work in total. I unfortunately tried to cut corners to speed the process and it lead me to "monkey patch" things. Then I had to roll back changes (without git at the time...) and think for real to solve problems...this is always a good lesson, always think then try, never try to patch blindly!
After that I couldn't leave my little toy project like that. So I coded sqrt, pow, factorial, and the chudnovsky method to calculate pi (a good test for the square root algorithm). I also started refactoring my test framework, added options to client. It feelt good tho to have a "cleaner env".
Now I post my code to github. It'll be easier to maintain it that way, people will be able to participate if they feel like it and recruiters might eventually find that while I'm not working, I hate to be inactive, I'm not binging netflix... (:

To be continued...

Roadmap
-------

 #. [V] simple add
 #. [V] simple sub (this was not "easy")
 #. [V] simple mul
 #. [V] simple div (this was a little bit harder)
 #. [V] parsing + syntax simplification + basic AST & error handling
 #. [V] "resolve" function (which gives the actual result)
 #. [V] putting things all together and testing the hell out
 #. [V] float handling (a little bit of a mindf***)
 #. [V] remove floor() and all mutiplication, modulo and division, so only additions ans substractions remain
 #. [V] refactor some parts + better testing framework
 #. [V] calculate pi using Gregory-Leibniz series
 #. [V] calculate pi using Nilakantha series
 #. [V] pow + factorial + sqrt
 #. [V] calculate pi using the Chudnovsky algorithm
 #. [V] scientific convention notation (only for end result)
 #. [ ] maybe try poetry so it's easy to have local dependencies in dedicated folders
 #. [ ] make the whole project OOB (or not? or just bistro? maybe tests also?) + refactor agayhn
 #. [ ] variables manipulation (set x 1 or x = 1)
 #. [ ] try to find a clean way to point where there is a mistake in the entry if any
 #. [ ] fraction notation = cos/sin/tan
