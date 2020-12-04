#!/bin/sh
find . -name __snapshots__ ! -path "./node_modules/*" -type d -print0| xargs -0 rm -r --
