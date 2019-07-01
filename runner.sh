until pideck; do
	echo "Server 'pideck' crashed with exit code $?. Respawning..." >&2
	sleep 1
done
