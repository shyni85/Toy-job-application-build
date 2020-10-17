from sqlalchemy import create_engine


class DbOperations:
    def __init__(self, url):
        self.engine = create_engine(url, echo=True)

    def dbinsert(self, table_object, job_id, job_name, salary):
        conn = self.engine.connect()
        ins = table_object.insert().values(id=job_id, name=job_name, salary=salary)
        result = conn.execute(ins)
        return result

    def selectall(self, table_object):
        conn = self.engine.connect()
        s = table_object.select()
        result = conn.execute(s)
        jobsget = result.fetchall()
        return jobsget

    def fetchjobdetails(self, table_object, jobid):
        conn = self.engine.connect()
        s = table_object.select().where(table_object.c.id == jobid)
        result = conn.execute(s)
        job_detail = result.fetchall()
        return job_detail

    def deletejob(self, table_object, jobid):
        conn = self.engine.connect()
        delete = table_object.delete().where(table_object.c.id == jobid)
        result = conn.execute(delete)
