from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, text
import  uvicorn
from  DbOperations import DbOperations


db = DbOperations("sqlite:///job_details.db")
meta = MetaData()
table_object = Table(
    'jobdetails', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('salary', String),
)
meta.create_all(db.engine)

app = FastAPI()
class Jobs(BaseModel):
    job_id: int
    job_name: str
    salary: int

# GET all jobs details in array of dictionary
@app.get("/jobs/get")
def get_complete_jobdetails():
    jobsget=db.selectall(table_object)
    return jobsget

# Listing the detail of one particular job
@app.get("/jobs/{jobid}")
def get_job_details(jobid: int ):
    job_detail = db.fetchjobdetails(table_object,jobid)
    return job_detail

#Adding new job
@app.put("/jobs/post")
def job_put(newjobs: Jobs):
    db.dbinsert(table_object,newjobs.job_id ,newjobs.job_name,newjobs.salary )
    return {"jobs": newjobs.job_id, "JobName": newjobs.job_name}

#Delete one job detail from database
@app.delete("/jobs/delete/{jobid}")
def delete_job( jobid: int):
    db.deletejob(table_object,jobid)
    return {"JobidDeleted": jobid}

# Calling uvicorn run
if __name__ == "__main__":
    uvicorn.run(app,host="127.0.0.1")
