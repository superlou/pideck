until `python3 server.py`; do
	echo "Server 'pideck' crashed with exit code $?. Respawning..." >&2
	sleep 1
done
