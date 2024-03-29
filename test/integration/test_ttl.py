# coding=UTF-8

"""
Tests the representation of TTLs in backup files.
"""

import lib
from run_backup import backup_and_restore

def put_ttl(key, ttl):
	"""
	Inserts the given key with the given TTL.
	"""
	lib.write_record(lib.SET, key, ["value"], ["value"], False, ttl)

def check_ttl(key, expected_ttl):
	"""
	Ensures that the given key has the given TTL.
	"""
	meta_key, meta_ttl, record = lib.read_record(lib.SET, key)
	lib.validate_record(key, record, ["value"], ["value"])
	lib.validate_meta(key, meta_key, meta_ttl, False, expected_ttl)

def check_expired(key):
	"""
	Ensures that the given key does not exist.
	"""
	assert not lib.test_record(lib.SET, key), "Key %s should not exist" % key

def test_no_ttl():
	"""
	Test without a TTL.
	"""
	backup_and_restore(
		lambda context: put_ttl(0, None),
		None,
		lambda context: check_ttl(0, None)
	)

def test_ttl():
	"""
	Test TTL without a delay.
	"""
	backup_and_restore(
		lambda context: put_ttl(1, 1000),
		None,
		lambda context: check_ttl(1, (900, 1000))
	)

def test_ttl_delay_10():
	"""
	Test TTL with a 10 second delay.
	"""
	backup_and_restore(
		lambda context: put_ttl(2, 1000),
		None,
		lambda context: check_ttl(2, (0, 990)),
		restore_delay=10
	)

def test_ttl_expired():
	"""
	Make sure that expired records are not restored. Works, because we prevent
	asd from expiring records (low-water-pct set to 10).
	"""
	backup_and_restore(
		lambda context: put_ttl(3, 5),
		None,
		lambda context: check_expired(3),
		restore_delay=10
	)
