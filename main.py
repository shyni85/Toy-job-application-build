from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, text
import  uvicorn

engine = create_engine('sqlite:///job_details.db', echo=True)

meta = MetaData()

students = Table(
    'students', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('salary', String),
)
meta.create_all(engine)

app = FastAPI()


class Jobs(BaseModel):
    job_id: int
    job_name: str
    salary: int


# GET all jobs details in array of dictionary
# fetchall function takes all rows in the select result
@app.get("/jobs/get")
def read_root():
    s = students.select()
    conn = engine.connect()
    result = conn.execute(s)
    jobsget = result.fetchall()
    return jobsget


# Listing the detail of one particular job
@app.get("/jobs/{jobid}")
def get_job_details(jobid: int):
    query = "SELECT * FROM students where id ==" + str(jobid)
    t = text(query)
    conn = engine.connect()
    result = conn.execute(t)
    job_detail = result.fetchone()
    return job_detail


@app.put("/jobs/post")
def job_put(newjobs: Jobs):
    ins = students.insert().values(id=newjobs.job_id, name=newjobs.job_name, salary=newjobs.salary)
    conn = engine.connect()
    result = conn.execute(ins)
    return {"jobs": newjobs.job_id, "JobName": newjobs.job_name}

if __name__ == "__main__" :
    uvicorn.run(app,host="127.0.0.1",port=8000)
