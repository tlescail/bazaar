from pydantic import BaseModel, Field

from bazaar.lib.proxmox import proxmox


class Node(BaseModel):
    node: str
    id: str
    
    maxcpu: int
    maxmem: int
    maxdisk: int
    
    status: str
    uptime: int
    cpu: float
    mem: int
    disk: int
    
class Qemu(BaseModel):
    vmid: int
    name: str
    template: int | None = None
    
    cpus: int
    maxmem: int
    maxdisk: int
    
    status: str
    uptime: int
    pid: int | None = None
    
    cpu: float
    mem: int
    disk: int
    
class VirtualMachine(Qemu):
    node: Node

class QemuClone(BaseModel):
    newid: int = Field(int(proxmox().cluster.nextid.get()))
    
    bwlimit: int | None = None
    description: str | None = None
    full: int = Field(0)
    format: str | None = None
    name: str | None = None
    pool: str | None = None
    snapname: str | None = None
    storage: str | None = None
    target: str | None = None
    
class TaskResult(BaseModel):
    exitstatus: str
    upid: str
    status: str
    starttime: int
    id: str
    type: str
    user: str
    pstart: int
    node: str
    pid: int    