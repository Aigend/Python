#include <Python.h>
#include <BD4A_if.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

char* Generate_CStr_From_PyStr(PyObject* str)
{
    PyObject* py_utf = PyUnicode_AsUTF8String(str);
    char* c_str = PyBytes_AsString(py_utf);
    printf("python dict key or value convert C str:%s\n", c_str);
    return c_str;
};

PyObject* Generate_Func_Args_PyDict(PyObject* dict, char* arg)
{
    PyObject* py_sv = Py_BuildValue("s", arg);
    PyObject* py_ut = PyUnicode_AsUTF8String(py_sv);
    char* name = PyBytes_AsString(py_ut);
    PyObject* py_value = NULL;
    PyObject* py_keys = PyDict_Keys(dict);
    for (int i = 0;i < PyList_Size(py_keys);i++) {
        PyObject* py_key = PyList_GetItem(py_keys, i);
        PyObject* py_utf = PyUnicode_AsUTF8String(py_key);
        char* result = PyBytes_AsString(py_utf);
        if (strcmp(result, name) == 0) {
            py_value = PyDict_GetItem(dict, py_key);
            break;
        };
    };
    return py_value;
};

PyObject* generate_result_dict(int result, PyObject* data_value)
{
    PyObject* result_dict = PyDict_New();
    PyObject* result_value = NULL;
    if (result == 0) {
        result_value = Py_BuildValue("s", "OK");
    }
    else {
        result_value = Py_BuildValue("s", "ERROR");
    }
    PyObject* result_key = Py_BuildValue("s", "result");
    PyDict_SetItem(result_dict, result_key, result_value);
    PyObject* code_key = Py_BuildValue("s", "code");
    PyObject* code_value = Py_BuildValue("i", result);
    PyDict_SetItem(result_dict, code_key, code_value);
    PyObject* data_key = Py_BuildValue("s", "data");
    PyDict_SetItem(result_dict, data_key, data_value);
    return result_dict;
};

void bd4a_dtc_data_callback_function(BD4A_BMS_DTC_STRUCT * status, ZOO_INT32 error_code, void *context)
{
	printf("@enter function %s@\n",__FUNCTION__);
}

void* bd4a_dtc_data_after_callback(void* args)
{
	printf("@enter function %s@\n",__FUNCTION__);
	return NULL;
}

void bd4a_status_callback_function(BD4A_STATUS_STRUCT * status, ZOO_INT32 error_code, void *context)
{
	printf("@enter function %s@\n",__FUNCTION__);
}

void* bd4a_status_after_callback(void* args)
{
	printf("@enter function %s@\n",__FUNCTION__);
	return NULL;
}

static PyObject* Py_BD4A_initialize(PyObject* self)
{
	printf("@enter function %s @\n", __FUNCTION__);
	int ec = BD4A_initialize();
	printf("@exit function %s @\n", __FUNCTION__);
	PyObject* data_value = PyDict_New();
	return generate_result_dict(ec, data_value);
}

static PyObject* Py_BD4A_initialize_req(PyObject* self)
{
	printf("@enter function %s @\n", __FUNCTION__);
	int ec = BD4A_initialize_req();
	printf("@exit function %s @\n", __FUNCTION__);
	PyObject* data_value = PyDict_New();
	return generate_result_dict(ec, data_value);
}

static PyObject* Py_BD4A_initialize_wait(PyObject* self, PyObject* args)
{
	printf("@enter function %s @\n", __FUNCTION__);
	PyObject* arg1;
	PyArg_ParseTuple(args, "O", &arg1);

	ZOO_INT32 timeout = PyLong_AsLong(arg1);
	printf("@begin call function %s @\n",__FUNCTION__);
	int ec = BD4A_initialize_wait(timeout);
	printf("@exit function %s @\n", __FUNCTION__);
	PyObject * data_value = PyDict_New();
	return generate_result_dict(ec, data_value);
}

static PyObject* Py_BD4A_terminate(PyObject* self)
{
	printf("@enter function %s @\n", __FUNCTION__);
	int ec = BD4A_terminate();
	printf("@exit function %s @\n", __FUNCTION__);
	PyObject* data_value = PyDict_New();
	return generate_result_dict(ec, data_value);
}

static PyObject* Py_BD4A_terminate_req(PyObject* self)
{
	printf("@enter function %s @\n", __FUNCTION__);
	int ec = BD4A_terminate_req();
	printf("@exit function %s @\n", __FUNCTION__);
	PyObject* data_value = PyDict_New();
	return generate_result_dict(ec, data_value);
}

static PyObject* Py_BD4A_terminate_wait(PyObject* self, PyObject* args)
{
	printf("@enter function %s @\n", __FUNCTION__);
	PyObject* arg1;
	PyArg_ParseTuple(args, "O", &arg1);

	ZOO_INT32 timeout = PyLong_AsLong(arg1);
	printf("@begin call function %s @\n",__FUNCTION__);
	int ec = BD4A_terminate_wait(timeout);
	printf("@exit function %s @\n", __FUNCTION__);
	PyObject * data_value = PyDict_New();
	return generate_result_dict(ec, data_value);
}

static PyObject* Py_BD4A_get_driver_state(PyObject* self, PyObject* args)
{
	printf("@enter function %s @\n", __FUNCTION__);
	PyObject* arg1;
	PyArg_ParseTuple(args, "O", &arg1);

	printf("@begin to generate ZOO_DRIVER_STATE_ENUM state@\n");
	ZOO_DRIVER_STATE_ENUM state = (ZOO_DRIVER_STATE_ENUM)PyLong_AsLong(arg1);
	printf("@begin call function %s @\n",__FUNCTION__);
	int ec = BD4A_get_driver_state(&state);
	printf("@exit function %s @\n", __FUNCTION__);
	PyObject * data_value = PyDict_New();
	return generate_result_dict(ec, data_value);
}

static PyObject* Py_BD4A_get_status(PyObject* self, PyObject* args)
{
	printf("@enter function %s @\n", __FUNCTION__);
	PyObject* arg1;
	PyArg_ParseTuple(args, "O", &arg1);
	PyObject* arg1_ZOO_DRIVER_STATE_ENUM = Generate_Func_Args_PyDict(arg1, "ZOO_DRIVER_STATE_ENUM");
	PyObject* arg1_state = Generate_Func_Args_PyDict(arg1_ZOO_DRIVER_STATE_ENUM, "state");
	PyObject* arg1_bms_sw_version = Generate_Func_Args_PyDict(arg1, "bms_sw_version");
	PyObject* arg1_connect_bms_state = Generate_Func_Args_PyDict(arg1, "connect_bms_state");
	PyObject* arg1_connect_matrix_state = Generate_Func_Args_PyDict(arg1, "connect_matrix_state");
	PyObject* arg1_matrix_sw_version = Generate_Func_Args_PyDict(arg1, "matrix_sw_version");
	PyObject* arg1_reflesh_progress_value = Generate_Func_Args_PyDict(arg1, "reflesh_progress_value");
	printf("@begin to generate BD4A_STATUS_STRUCT status@\n");
	BD4A_STATUS_STRUCT status;
	memset(&status, 0, sizeof(BD4A_STATUS_STRUCT));
	status.state = (ZOO_DRIVER_STATE_ENUM)PyLong_AsLong(arg1_state);
	strcpy(status.bms_sw_version, Generate_CStr_From_PyStr(arg1_bms_sw_version));
	status.connect_bms_state = PyLong_AsLong(arg1_connect_bms_state);
	status.connect_matrix_state = PyLong_AsLong(arg1_connect_matrix_state);
	strcpy(status.matrix_sw_version, Generate_CStr_From_PyStr(arg1_matrix_sw_version));
	status.reflesh_progress_value = PyLong_AsLong(arg1_reflesh_progress_value);
	printf("@begin call function %s @\n",__FUNCTION__);
	int ec = BD4A_get_status(&status);
	printf("@exit function %s @\n", __FUNCTION__);
	PyObject * data_value = PyDict_New();
	return generate_result_dict(ec, data_value);
}

static PyObject* Py_BD4A_change_to_work_mode(PyObject* self)
{
	printf("@enter function %s @\n", __FUNCTION__);
	int ec = BD4A_change_to_work_mode();
	printf("@exit function %s @\n", __FUNCTION__);
	PyObject* data_value = PyDict_New();
	return generate_result_dict(ec, data_value);
}

static PyObject* Py_BD4A_change_to_debug_mode(PyObject* self)
{
	printf("@enter function %s @\n", __FUNCTION__);
	int ec = BD4A_change_to_debug_mode();
	printf("@exit function %s @\n", __FUNCTION__);
	PyObject* data_value = PyDict_New();
	return generate_result_dict(ec, data_value);
}

static PyObject* Py_BD4A_download_machine_constants(PyObject* self)
{
	printf("@enter function %s @\n", __FUNCTION__);
	int ec = BD4A_download_machine_constants();
	printf("@exit function %s @\n", __FUNCTION__);
	PyObject* data_value = PyDict_New();
	return generate_result_dict(ec, data_value);
}

static PyObject* Py_BD4A_get_matrix_sw_version(PyObject* self, PyObject* args)
{
	printf("@enter function %s @\n", __FUNCTION__);
	PyObject* arg1;
	PyArg_ParseTuple(args, "O", &arg1);

	ZOO_CHAR version[BD4A_BUFFER_LENTH];
	strcpy(version, Generate_CStr_From_PyStr(arg1));
	printf("@begin call function %s @\n",__FUNCTION__);
	int ec = BD4A_get_matrix_sw_version(version);
	printf("@exit function %s @\n", __FUNCTION__);
	PyObject * data_value = PyDict_New();
	return generate_result_dict(ec, data_value);
}

static PyObject* Py_BD4A_get_bms_sw_version(PyObject* self, PyObject* args)
{
	printf("@enter function %s @\n", __FUNCTION__);
	PyObject* arg1;
	PyArg_ParseTuple(args, "O", &arg1);

	ZOO_CHAR version[BD4A_BUFFER_LENTH];
	strcpy(version, Generate_CStr_From_PyStr(arg1));
	printf("@begin call function %s @\n",__FUNCTION__);
	int ec = BD4A_get_bms_sw_version(version);
	printf("@exit function %s @\n", __FUNCTION__);
	PyObject * data_value = PyDict_New();
	return generate_result_dict(ec, data_value);
}

static PyObject* Py_BD4A_get_dtc_data(PyObject* self, PyObject* args)
{
	printf("@enter function %s @\n", __FUNCTION__);
	PyObject* arg1;
	PyArg_ParseTuple(args, "O", &arg1);
	PyObject* arg1_BD4A_DTC_DATA_STRUCT = Generate_Func_Args_PyDict(arg1, "BD4A_DTC_DATA_STRUCT");
	PyObject* arg1_p160244 = Generate_Func_Args_PyDict(arg1_BD4A_DTC_DATA_STRUCT, "p160244");
	PyObject* arg1_p160244_data = Generate_Func_Args_PyDict(arg1_p160244, "data");
	PyObject* arg1_p160244_id = Generate_Func_Args_PyDict(arg1_p160244, "id");
	PyObject* arg1_p160244_number = Generate_Func_Args_PyDict(arg1_p160244, "number");
	PyObject* arg1_p161d21 = Generate_Func_Args_PyDict(arg1_BD4A_DTC_DATA_STRUCT, "p161d21");
	PyObject* arg1_p161d21_data = Generate_Func_Args_PyDict(arg1_p161d21, "data");
	PyObject* arg1_p161d21_id = Generate_Func_Args_PyDict(arg1_p161d21, "id");
	PyObject* arg1_p161d21_number = Generate_Func_Args_PyDict(arg1_p161d21, "number");
	PyObject* arg1_p161e00 = Generate_Func_Args_PyDict(arg1_BD4A_DTC_DATA_STRUCT, "p161e00");
	PyObject* arg1_p161e00_data = Generate_Func_Args_PyDict(arg1_p161e00, "data");
	PyObject* arg1_p161e00_id = Generate_Func_Args_PyDict(arg1_p161e00, "id");
	PyObject* arg1_p161e00_number = Generate_Func_Args_PyDict(arg1_p161e00, "number");
	PyObject* arg1_p16aa62 = Generate_Func_Args_PyDict(arg1_BD4A_DTC_DATA_STRUCT, "p16aa62");
	PyObject* arg1_p16aa62_data = Generate_Func_Args_PyDict(arg1_p16aa62, "data");
	PyObject* arg1_p16aa62_id = Generate_Func_Args_PyDict(arg1_p16aa62, "id");
	PyObject* arg1_p16aa62_number = Generate_Func_Args_PyDict(arg1_p16aa62, "number");
	PyObject* arg1_p16b821 = Generate_Func_Args_PyDict(arg1_BD4A_DTC_DATA_STRUCT, "p16b821");
	PyObject* arg1_p16b821_data = Generate_Func_Args_PyDict(arg1_p16b821, "data");
	PyObject* arg1_p16b821_id = Generate_Func_Args_PyDict(arg1_p16b821, "id");
	PyObject* arg1_p16b821_number = Generate_Func_Args_PyDict(arg1_p16b821, "number");
	PyObject* arg1_p16b922 = Generate_Func_Args_PyDict(arg1_BD4A_DTC_DATA_STRUCT, "p16b922");
	PyObject* arg1_p16b922_data = Generate_Func_Args_PyDict(arg1_p16b922, "data");
	PyObject* arg1_p16b922_id = Generate_Func_Args_PyDict(arg1_p16b922, "id");
	PyObject* arg1_p16b922_number = Generate_Func_Args_PyDict(arg1_p16b922, "number");
	PyObject* arg1_p16bc21 = Generate_Func_Args_PyDict(arg1_BD4A_DTC_DATA_STRUCT, "p16bc21");
	PyObject* arg1_p16bc21_data = Generate_Func_Args_PyDict(arg1_p16bc21, "data");
	PyObject* arg1_p16bc21_id = Generate_Func_Args_PyDict(arg1_p16bc21, "id");
	PyObject* arg1_p16bc21_number = Generate_Func_Args_PyDict(arg1_p16bc21, "number");
	PyObject* arg1_p16bd22 = Generate_Func_Args_PyDict(arg1_BD4A_DTC_DATA_STRUCT, "p16bd22");
	PyObject* arg1_p16bd22_data = Generate_Func_Args_PyDict(arg1_p16bd22, "data");
	PyObject* arg1_p16bd22_id = Generate_Func_Args_PyDict(arg1_p16bd22, "id");
	PyObject* arg1_p16bd22_number = Generate_Func_Args_PyDict(arg1_p16bd22, "number");
	PyObject* arg1_p16be00 = Generate_Func_Args_PyDict(arg1_BD4A_DTC_DATA_STRUCT, "p16be00");
	PyObject* arg1_p16be00_data = Generate_Func_Args_PyDict(arg1_p16be00, "data");
	PyObject* arg1_p16be00_id = Generate_Func_Args_PyDict(arg1_p16be00, "id");
	PyObject* arg1_p16be00_number = Generate_Func_Args_PyDict(arg1_p16be00, "number");
	PyObject* arg1_p16f792 = Generate_Func_Args_PyDict(arg1_BD4A_DTC_DATA_STRUCT, "p16f792");
	PyObject* arg1_p16f792_data = Generate_Func_Args_PyDict(arg1_p16f792, "data");
	PyObject* arg1_p16f792_id = Generate_Func_Args_PyDict(arg1_p16f792, "id");
	PyObject* arg1_p16f792_number = Generate_Func_Args_PyDict(arg1_p16f792, "number");
	PyObject* arg1_u21bb82 = Generate_Func_Args_PyDict(arg1_BD4A_DTC_DATA_STRUCT, "u21bb82");
	PyObject* arg1_u21bb82_data = Generate_Func_Args_PyDict(arg1_u21bb82, "data");
	PyObject* arg1_u21bb82_id = Generate_Func_Args_PyDict(arg1_u21bb82, "id");
	PyObject* arg1_u21bb82_number = Generate_Func_Args_PyDict(arg1_u21bb82, "number");
	printf("@begin to generate BD4A_BMS_DTC_STRUCT bms_dtc_data@\n");
	BD4A_BMS_DTC_STRUCT bms_dtc_data;
	memset(&bms_dtc_data, 0, sizeof(BD4A_BMS_DTC_STRUCT));
	strcpy(bms_dtc_data.p160244.data, Generate_CStr_From_PyStr(arg1_p160244_data));
	strcpy(bms_dtc_data.p160244.id, Generate_CStr_From_PyStr(arg1_p160244_id));
	strcpy(bms_dtc_data.p160244.number, Generate_CStr_From_PyStr(arg1_p160244_number));
	strcpy(bms_dtc_data.p161d21.data, Generate_CStr_From_PyStr(arg1_p161d21_data));
	strcpy(bms_dtc_data.p161d21.id, Generate_CStr_From_PyStr(arg1_p161d21_id));
	strcpy(bms_dtc_data.p161d21.number, Generate_CStr_From_PyStr(arg1_p161d21_number));
	strcpy(bms_dtc_data.p161e00.data, Generate_CStr_From_PyStr(arg1_p161e00_data));
	strcpy(bms_dtc_data.p161e00.id, Generate_CStr_From_PyStr(arg1_p161e00_id));
	strcpy(bms_dtc_data.p161e00.number, Generate_CStr_From_PyStr(arg1_p161e00_number));
	strcpy(bms_dtc_data.p16aa62.data, Generate_CStr_From_PyStr(arg1_p16aa62_data));
	strcpy(bms_dtc_data.p16aa62.id, Generate_CStr_From_PyStr(arg1_p16aa62_id));
	strcpy(bms_dtc_data.p16aa62.number, Generate_CStr_From_PyStr(arg1_p16aa62_number));
	strcpy(bms_dtc_data.p16b821.data, Generate_CStr_From_PyStr(arg1_p16b821_data));
	strcpy(bms_dtc_data.p16b821.id, Generate_CStr_From_PyStr(arg1_p16b821_id));
	strcpy(bms_dtc_data.p16b821.number, Generate_CStr_From_PyStr(arg1_p16b821_number));
	strcpy(bms_dtc_data.p16b922.data, Generate_CStr_From_PyStr(arg1_p16b922_data));
	strcpy(bms_dtc_data.p16b922.id, Generate_CStr_From_PyStr(arg1_p16b922_id));
	strcpy(bms_dtc_data.p16b922.number, Generate_CStr_From_PyStr(arg1_p16b922_number));
	strcpy(bms_dtc_data.p16bc21.data, Generate_CStr_From_PyStr(arg1_p16bc21_data));
	strcpy(bms_dtc_data.p16bc21.id, Generate_CStr_From_PyStr(arg1_p16bc21_id));
	strcpy(bms_dtc_data.p16bc21.number, Generate_CStr_From_PyStr(arg1_p16bc21_number));
	strcpy(bms_dtc_data.p16bd22.data, Generate_CStr_From_PyStr(arg1_p16bd22_data));
	strcpy(bms_dtc_data.p16bd22.id, Generate_CStr_From_PyStr(arg1_p16bd22_id));
	strcpy(bms_dtc_data.p16bd22.number, Generate_CStr_From_PyStr(arg1_p16bd22_number));
	strcpy(bms_dtc_data.p16be00.data, Generate_CStr_From_PyStr(arg1_p16be00_data));
	strcpy(bms_dtc_data.p16be00.id, Generate_CStr_From_PyStr(arg1_p16be00_id));
	strcpy(bms_dtc_data.p16be00.number, Generate_CStr_From_PyStr(arg1_p16be00_number));
	strcpy(bms_dtc_data.p16f792.data, Generate_CStr_From_PyStr(arg1_p16f792_data));
	strcpy(bms_dtc_data.p16f792.id, Generate_CStr_From_PyStr(arg1_p16f792_id));
	strcpy(bms_dtc_data.p16f792.number, Generate_CStr_From_PyStr(arg1_p16f792_number));
	strcpy(bms_dtc_data.u21bb82.data, Generate_CStr_From_PyStr(arg1_u21bb82_data));
	strcpy(bms_dtc_data.u21bb82.id, Generate_CStr_From_PyStr(arg1_u21bb82_id));
	strcpy(bms_dtc_data.u21bb82.number, Generate_CStr_From_PyStr(arg1_u21bb82_number));
	printf("@begin call function %s @\n",__FUNCTION__);
	int ec = BD4A_get_dtc_data(&bms_dtc_data);
	printf("@exit function %s @\n", __FUNCTION__);
	PyObject * data_value = PyDict_New();
	return generate_result_dict(ec, data_value);
}

static PyObject* Py_BD4A_reflesh(PyObject* self, PyObject* args)
{
	printf("@enter function %s @\n", __FUNCTION__);
	PyObject* arg1;
	PyArg_ParseTuple(args, "O", &arg1);

	ZOO_CHAR bms_sw_version[BD4A_BUFFER_LENTH];
	strcpy(bms_sw_version, Generate_CStr_From_PyStr(arg1));
	printf("@begin call function %s @\n",__FUNCTION__);
	int ec = BD4A_reflesh(bms_sw_version);
	printf("@exit function %s @\n", __FUNCTION__);
	PyObject * data_value = PyDict_New();
	return generate_result_dict(ec, data_value);
}

static PyObject* Py_BD4A_dtc_data_subscribe(PyObject* self, PyObject* args)
{
	printf("@enter function %s @\n", __FUNCTION__);
	PyObject* arg1;
	PyObject* arg2;
	PyObject* arg3;
	PyArg_ParseTuple(args, "OOO", &arg1, &arg2, &arg3);

	ZOO_HANDLE handle = PyLong_AsLong(arg2);
	int context = PyLong_AsLong(arg3);
	printf("@begin call function %s @\n",__FUNCTION__);
	int ec = BD4A_dtc_data_subscribe(bd4a_dtc_data_callback_function, &handle, &context);
	printf("@exit function %s @\n", __FUNCTION__);
	PyObject * data_value = PyDict_New();
	return generate_result_dict(ec, data_value);
}

static PyObject* Py_BD4A_dtc_data_unsubscribe(PyObject* self, PyObject* args)
{
	printf("@enter function %s @\n", __FUNCTION__);
	PyObject* arg1;
	PyArg_ParseTuple(args, "O", &arg1);

	ZOO_HANDLE handle = PyLong_AsLong(arg1);
	printf("@begin call function %s @\n",__FUNCTION__);
	int ec = BD4A_dtc_data_unsubscribe(handle);
	printf("@exit function %s @\n", __FUNCTION__);
	PyObject * data_value = PyDict_New();
	return generate_result_dict(ec, data_value);
}

static PyObject* Py_BD4A_status_subscribe(PyObject* self, PyObject* args)
{
	printf("@enter function %s @\n", __FUNCTION__);
	PyObject* arg1;
	PyObject* arg2;
	PyObject* arg3;
	PyArg_ParseTuple(args, "OOO", &arg1, &arg2, &arg3);

	ZOO_HANDLE handle = PyLong_AsLong(arg2);
	int context = PyLong_AsLong(arg3);
	printf("@begin call function %s @\n",__FUNCTION__);
	int ec = BD4A_status_subscribe(bd4a_status_callback_function, &handle, &context);
	printf("@exit function %s @\n", __FUNCTION__);
	PyObject * data_value = PyDict_New();
	return generate_result_dict(ec, data_value);
}

static PyObject* Py_BD4A_status_unsubscribe(PyObject* self, PyObject* args)
{
	printf("@enter function %s @\n", __FUNCTION__);
	PyObject* arg1;
	PyArg_ParseTuple(args, "O", &arg1);

	ZOO_HANDLE handle = PyLong_AsLong(arg1);
	printf("@begin call function %s @\n",__FUNCTION__);
	int ec = BD4A_status_unsubscribe(handle);
	printf("@exit function %s @\n", __FUNCTION__);
	PyObject * data_value = PyDict_New();
	return generate_result_dict(ec, data_value);
}

static char Py_BD4A_docs[] = "BD4A:software platform for applications!!";

static PyMethodDef BD4A_methods[] = {
	{"Py_BD4A_initialize", (PyCFunction)Py_BD4A_initialize, METH_NOARGS, Py_BD4A_docs},
	{"Py_BD4A_initialize_req", (PyCFunction)Py_BD4A_initialize_req, METH_NOARGS, Py_BD4A_docs},
	{"Py_BD4A_initialize_wait", (PyCFunction)Py_BD4A_initialize_wait, METH_VARARGS, Py_BD4A_docs},
	{"Py_BD4A_terminate", (PyCFunction)Py_BD4A_terminate, METH_NOARGS, Py_BD4A_docs},
	{"Py_BD4A_terminate_req", (PyCFunction)Py_BD4A_terminate_req, METH_NOARGS, Py_BD4A_docs},
	{"Py_BD4A_terminate_wait", (PyCFunction)Py_BD4A_terminate_wait, METH_VARARGS, Py_BD4A_docs},
	{"Py_BD4A_get_driver_state", (PyCFunction)Py_BD4A_get_driver_state, METH_VARARGS, Py_BD4A_docs},
	{"Py_BD4A_get_status", (PyCFunction)Py_BD4A_get_status, METH_VARARGS, Py_BD4A_docs},
	{"Py_BD4A_change_to_work_mode", (PyCFunction)Py_BD4A_change_to_work_mode, METH_NOARGS, Py_BD4A_docs},
	{"Py_BD4A_change_to_debug_mode", (PyCFunction)Py_BD4A_change_to_debug_mode, METH_NOARGS, Py_BD4A_docs},
	{"Py_BD4A_download_machine_constants", (PyCFunction)Py_BD4A_download_machine_constants, METH_NOARGS, Py_BD4A_docs},
	{"Py_BD4A_get_matrix_sw_version", (PyCFunction)Py_BD4A_get_matrix_sw_version, METH_VARARGS, Py_BD4A_docs},
	{"Py_BD4A_get_bms_sw_version", (PyCFunction)Py_BD4A_get_bms_sw_version, METH_VARARGS, Py_BD4A_docs},
	{"Py_BD4A_get_dtc_data", (PyCFunction)Py_BD4A_get_dtc_data, METH_VARARGS, Py_BD4A_docs},
	{"Py_BD4A_reflesh", (PyCFunction)Py_BD4A_reflesh, METH_VARARGS, Py_BD4A_docs},
	{"Py_BD4A_dtc_data_subscribe", (PyCFunction)Py_BD4A_dtc_data_subscribe, METH_VARARGS, Py_BD4A_docs},
	{"Py_BD4A_dtc_data_unsubscribe", (PyCFunction)Py_BD4A_dtc_data_unsubscribe, METH_VARARGS, Py_BD4A_docs},
	{"Py_BD4A_status_subscribe", (PyCFunction)Py_BD4A_status_subscribe, METH_VARARGS, Py_BD4A_docs},
	{"Py_BD4A_status_unsubscribe", (PyCFunction)Py_BD4A_status_unsubscribe, METH_VARARGS, Py_BD4A_docs},
	{ NULL, NULL, 0, NULL}
};

static struct PyModuleDef BD4A_module = {
	PyModuleDef_HEAD_INIT,
	"BD4A_Py",             /* name of module */
	"BD4A module doc",  /* module documentation, may be NULL */
	-1,                 /* size of per-interpreter state of the module,or -1 if the module keeps state in global variables. */
	BD4A_methods
};

PyMODINIT_FUNC PyInit_BD4A_Py(void){
	return PyModule_Create(&BD4A_module);
}

