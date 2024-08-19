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
