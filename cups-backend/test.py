import cups 

def test_job():
    conn = cups.Connection()
    attrs = conn.getJobAttributes(212)
    print(attrs)

test_job()
