GET  /programs
GET  /services
GET  /services/{service_name}/status
POST /services/{service_name}/start
POST /services/{service_name}/stop
POST /services/{service_name}/activity

- validate service name
- call runtime.start()
- call runtime.stop()
- update activity state
- return status objects

@router.post("/services/{name}/start")
def start_service(name: str):
    service = registry.get(name)
    runtime.start(service)
    state.mark_started(name)
    return {"service": name, "status": "starting"}