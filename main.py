from fastapi import FastAPI
from routers import user, blog, stuff
import models
import database

SHAMz = FastAPI(title="SHAMMAH & JAH-MAN",
                description="For ALL things work together for good to them that love GOD, to them who are the called according to HIS purpose: Romans 8:28 ;)")

models.Base.metadata.create_all(bind=database.engine)

SHAMz.include_router(router=stuff.SHAMz)
SHAMz.include_router(router=user.router)
SHAMz.include_router(router=blog.router)
