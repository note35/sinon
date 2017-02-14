"""
Copyright (c) 2016-2017, Kir Chou
https://github.com/note35/sinon/blob/master/LICENSE

This is an example integration test for example flask application

from test001 to test005, there are classic integration test
from test101 to test105, there are classic integration test with sinon spy
In test201, there is an example by using sinon stub
In test301, there is an example by using sinon mock
"""

#for temporary database
import os
import tempfile

#for unittest
import json
import unittest
import sinon

#subject
import flaskr 
from utils.absdb import TodoModel


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        flaskr.app.config["TESTING"] = True
        self.db_fd, flaskr.app.config["DATABASE"] = tempfile.mkstemp()

        # initialize database
        tmodel = TodoModel()
        with flaskr.app.app_context():
            tmodel.setup_init_data()

        self.app = flaskr.app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config["DATABASE"])

    # Classic RESTful Unittest
    def test001_get_list(self):
        # after executing get request, it should return expected result
        rv = self.app.get("/todos")
        expect_rv = {
            '1': {'Name': 'todo1', 'id': 1, 'Content': 'build an API'},
            '2': {'Name': 'todo2', 'id': 2, 'Content': '?????'},
            '3': {'Name': 'todo3', 'id': 3, 'Content': 'profit!'}
        }
        self.assertEqual(expect_rv, json.loads(rv.data.decode("utf-8")))

    def test002_get(self):
        # after executing get request, it should return expected result
        rv = self.app.get("/todos/1")
        expect_rv = {'Content': 'build an API', 'Name': 'todo1', 'id': 1}
        self.assertEqual(expect_rv, json.loads(rv.data.decode("utf-8")))

    def test003_delete(self):
        # (1) executing del request
        self.app.delete("/todos/1")
        # (2) after executing get request, it should return 404 result
        rv = self.app.get("/todos/1")
        expect_rv = {'message': 'Todo 1 doesn not exist. You have requested this URI [/todos/1] but did you mean /todos/<todo_id> or /todos ?'}
        self.assertEqual(expect_rv, json.loads(rv.data.decode("utf-8")))

    def test004_put_update(self):
        # (1) executing put request
        self.app.put("/todos/1", data={"name":"new name", "content":"new content"})

        # (2) then executing get request, it should return updated result
        rv = self.app.get("/todos/1")
        expect_rv = {'Content': 'new content', 'id': 1, 'Name': 'new name'}
        self.assertEqual(expect_rv, json.loads(rv.data.decode("utf-8")))

    def test005_put_new(self):
        # (1) before executing put request, it should return 404 result
        rv = self.app.get("/todos/4")
        expect_rv = {'message': 'Todo 4 doesn not exist. You have requested this URI [/todos/4] but did you mean /todos/<todo_id> or /todos ?'}
        self.assertEqual(expect_rv, json.loads(rv.data.decode("utf-8")))

        # (2) then executing put request to add new content
        self.app.put("/todos/4", data={"name":"new name", "content":"new content"})

        # (3) executing get request again, it should return updated result
        rv = self.app.get("/todos/4")
        expect_rv = {'Name': 'new name', 'Content': 'new content', 'id': 4}
        self.assertEqual(expect_rv, json.loads(rv.data.decode("utf-8")))

    # RESTful Unittest with Sinon Spy
    @sinon.test
    def test101_get_list(self):
        # (0) using spy on related function
        spy_tmodel_gtl = sinon.spy(TodoModel, "get_todo_list")

        # (1) after executing get request, it should return expected result
        rv = self.app.get("/todos")
        expect_rv = {
            '1': {'Name': 'todo1', 'id': 1, 'Content': 'build an API'},
            '2': {'Name': 'todo2', 'id': 2, 'Content': '?????'},
            '3': {'Name': 'todo3', 'id': 3, 'Content': 'profit!'}
        }
        self.assertEqual(expect_rv, json.loads(rv.data.decode("utf-8")))

        # (2) furthermore, using spy to check this execution
        sinon.assertion.calledOnce(spy_tmodel_gtl)

    @sinon.test
    def test102_get(self):
        # (0) using spy on related functions
        spy_flaskr_abort = sinon.spy(flaskr, "abort_if_todo_doesnt_exist")
        spy_tmodel_gt = sinon.spy(TodoModel, "get_todo")

        # (1) after executing get request, it should return expected result
        rv = self.app.get("/todos/1")
        expect_rv = {'Content': 'build an API', 'Name': 'todo1', 'id': 1}
        self.assertTrue(expect_rv, json.loads(rv.data.decode("utf-8")))

        # (2) furthermore, using spy to check this execution
        sinon.assertion.calledOnce(spy_flaskr_abort)
        sinon.assertion.calledWith(spy_flaskr_abort, "1")
        sinon.assertion.calledTwice(spy_tmodel_gt) #query twice: check exist + get value
        sinon.assertion.alwaysCalledWith(spy_tmodel_gt, "1")
        sinon.assertion.callOrder(spy_flaskr_abort, spy_tmodel_gt, spy_tmodel_gt)

    @sinon.test
    def test103_delete(self):
        # (0) using spy on related functions
        spy_flaskr_abort = sinon.spy(flaskr, "abort_if_todo_doesnt_exist")
        spy_tmodel_gt = sinon.spy(TodoModel, "get_todo")
        spy_tmodel_dt = sinon.spy(TodoModel, "del_todo")

        # (1) after executing del request, using spy to check this execution
        self.app.delete("/todos/1")
        sinon.assertion.calledOnce(spy_flaskr_abort)
        sinon.assertion.calledWith(spy_flaskr_abort, "1")
        sinon.assertion.calledOnce(spy_tmodel_gt)
        sinon.assertion.alwaysCalledWith(spy_tmodel_gt, "1")
        sinon.assertion.calledOnce(spy_tmodel_dt)
        sinon.assertion.alwaysCalledWith(spy_tmodel_dt, "1")

        # (2) after executing get request, it should return 404 result
        rv = self.app.get("/todos/1")
        expect_rv = {'message': 'Todo 1 doesn not exist. You have requested this URI [/todos/1] but did you mean /todos/<todo_id> or /todos ?'}
        self.assertEqual(expect_rv, json.loads(rv.data.decode("utf-8")))

    @sinon.test
    def test104_put_update(self):
        # (0) using spy on related function
        spy_tmodel_pt = sinon.spy(TodoModel, "put_todo")

        # (1) after executing put request, using spy to check this execution
        self.app.put("/todos/1", data={"name":"new name", "content":"new content"})
        sinon.assertion.calledOnce(spy_tmodel_pt)
        sinon.assertion.alwaysCalledWith(spy_tmodel_pt, "1", "new name", "new content")

        # (2) after executing get request, it should return updated result
        rv = self.app.get("/todos/1")
        expect_rv = {'Content': 'new content', 'id': 1, 'Name': 'new name'}
        self.assertEqual(expect_rv, json.loads(rv.data.decode("utf-8")))

    @sinon.test
    def test105_put_new(self):
        # (0) using spy on related function
        spy_tmodel_pt = sinon.spy(TodoModel, "put_todo")

        # (1) after executing get request, it should return 404 result
        rv = self.app.get("/todos/4")
        expect_rv = {'message': 'Todo 4 doesn not exist. You have requested this URI [/todos/4] but did you mean /todos/<todo_id> or /todos ?'}
        self.assertEqual(expect_rv, json.loads(rv.data.decode("utf-8")))

        # (2) after executing put request, using spy to check this execution
        self.app.put("/todos/4", data={"name":"new name", "content":"new content"})
        sinon.assertion.calledOnce(spy_tmodel_pt)
        sinon.assertion.alwaysCalledWith(spy_tmodel_pt, "4", "new name", "new content")

        # (3) after executing get request, it should return the new put result
        rv = self.app.get("/todos/4")
        expect_rv = {'Name': 'new name', 'Content': 'new content', 'id': 4}
        self.assertEqual(expect_rv, json.loads(rv.data.decode("utf-8")))

    # RESTful unittest with Sinon Stub
    @sinon.test
    def test201_stub_get_todo(self):
        # (1) stub get_todo and giving prepared fake return value
        stub_tmodel_gt = sinon.stub(TodoModel, "get_todo")
        fake_rv = (0, "null", "result for unittest without connecting to database") #preparing fake return
        stub_tmodel_gt.withArgs("1").returns(fake_rv)

        # (2) after executing get request, it should return expected fake value
        rv = self.app.get("/todos/1")
        expect_rv = {'Name': 'null', 'id': 0, 'Content': 'result for unittest without connecting to database'}
        self.assertEqual(expect_rv, json.loads(rv.data.decode("utf-8")))

    # RESTful unittest with Sinon Mock
    @sinon.test
    def test301_mock_tmodel(self):
        # (0) preparing mock and stub unrelated function
        stub_flaskr_abort = sinon.stub(flaskr, "abort_if_todo_doesnt_exist") #ignore unrelated function
        mock_tmodel = sinon.mock(TodoModel)

        # (1) stub get_todo function
        # giving fake return to make program able to execute
        fake_rv = (0, "null", "result for unittest without really connecting to database") #preparing fake return
        expect_gt = mock_tmodel.expects("get_todo").returns(fake_rv)
        self.app.get("/todos/1")
        sinon.assertion.calledOnce(expect_gt)

        # (2) stub del_todo function
        expect_dt = mock_tmodel.expects("del_todo")
        self.app.delete("/todos/1")
        sinon.assertion.calledOnce(expect_dt)

        # (3) stub put_todo function
        expect_pt = mock_tmodel.expects("put_todo")
        self.app.put("/todos/1", data={"name":"new name", "content":"new content"})
        sinon.assertion.calledOnce(expect_pt)


if __name__ == '__main__':
    unittest.main()
