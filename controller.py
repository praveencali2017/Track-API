from flask import Flask, request
from flask_restful import Resource, Api
from db_helper import DBHelper
from utils import get_defaults
app=Flask(__name__)
track_api=Api(app)




class Track(Resource):
    """
    Tracks' table CRUD operations
    """
    def get(self, track_id=None):
        """
        Fetches all records
        :return: Response
        """
        db_helper=DBHelper()
        if track_id:
            result=db_helper.get_all('tracks',"*","TrackId= '{}'".format(track_id))
        else:
            result = db_helper.get_all('tracks', "*")
        if result is Exception:
            return {"msg":str(result)}
        return {"data":result}

    def put(self):
        """
        Updates the record
        :return:Response
        """
        data=request.get_json()
        try:
            track_id=""
            columns={}
            for key, value in data.items():
                if key=="TrackId":
                   track_id=data[key]
                else:
                   columns[key]=value
            db_helper = DBHelper()
            result=db_helper.update("tracks",columns,"TrackId= {}".format(track_id))
            return result
        except Exception as e:
            return {"msg":str(e)}

    def delete(self):
        """
        Deletes the record
        :return:
        """
        data = request.get_json()
        try:
            track_id=data["TrackId"]
            db_helper = DBHelper()
            result = db_helper.delete("tracks","*","TrackId= {}".format(track_id))
            return result
        except Exception as e:
            return {"msg":str(e)}

    def post(self):
        """
        Insert the new record
        :return:
        """
        data=request.get_json()
        try:
            db_helper = DBHelper()
            result = db_helper.insert("tracks",data)
            return result
        except Exception as e:
            return {"msg":str(e)}



class Track_Name_Composer(Resource):
    """
    Search Operation for the given Track's name or composer name
    """
    def get(self, name_composer):
        db_helper=DBHelper()
        result=db_helper.get_all('tracks',"*", "Name like '%{}%'".format(name_composer)+" OR Composer like '%{}%'".format(name_composer))
        if result is Exception:
            return {"msg":str(result)}
        return {"data":result}


### Resource Mapping to the endpoints
track_api.add_resource(Track,'/tracks/<track_id>/',"/tracks")
track_api.add_resource(Track_Name_Composer,'/tracks/<name_composer>')

### App Main Block
if __name__=='__main__':
    app.run(port=get_defaults("port"))