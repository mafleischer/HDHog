
# HDHog

1. [About](#about)
1. [Features](#features)
3. [Usage](#usage)
4. [Screenshots](#screenshots)
5. [Notes](#notes)

Browse a folder, list files and subfolders **sorted by size accross the directory tree** so that you see the biggest first.

## About <a name="about"></a>
One motivation for this tool was to conveniently find big disk space consumers in a folder and
delete them. To my surprise, there is not really something free out there for this task.


Only tested under Linux (Ubuntu) so far, but since all file operations are written generically, theoretically it should work for all OSes that that Python supports and that have Tk, though.

## Features <a name="features"></a>
- Browse views
    - [x] File list
    - [x] Folder list
    - [x] View as tree

## Usage <a name="usage"></a>

Install from PyPi:
```shell
pip3 install hdhog
```
and run ``hdhog`` in a terminal.


Or clone repository an install:
```shell
git clone https://github.com/mafleischer/HDHog
cd HDHog
pip3 install ./
```
and run ``hdhog`` in a terminal.

## Screenshots <a name="screenshots"></a>

<table>
    <!-- <style>
        th{background-color:#e2fce6;}
        td{background-color:#fff9f3;}
    </style> -->
    <tr>
        <!-- github raw links used so this README is rendered on PyPi too -->
        <th style="background-color: #e2fce6" >View files</th> <!-- color Nyanza -->
        <td style="background-color: #fff9f3" align="center"><img src="https://raw.githubusercontent.com/mafleischer/HDHog/master/doc/img/files.png" alt="View files"></img></td> <!--  color Floral White -->
    </tr>
    <tr>
        <th style="background-color: #e2fce6" >View folders</th>
        <td style="background-color: #fff9f3" align="center"><img src="https://raw.githubusercontent.com/mafleischer/HDHog/master/doc/img/dirs.png" alt="View folders"></img></td>
    </tr>
    <tr>
        <th style="background-color: #e2fce6" >View as tree</th>
        <td style="background-color: #fff9f3" align="center"><img src="https://raw.githubusercontent.com/mafleischer/HDHog/master/doc/img/tree.png" alt="View as tree"></img></td>
    </tr>
 </table>

## Notes <a name="notes"></a>
- Symlinks are ignored and are not displayed for now
- At first, focus was only on finding and listing files. The tree view is really not optimal but sufficient for now