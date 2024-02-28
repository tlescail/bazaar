from typing_extensions import Annotated
from typing import List
from fastapi import APIRouter, Depends
from proxmoxer import ProxmoxAPI
from proxmoxer.tools import Tasks

from bazaar.lib.proxmox import proxmox
from bazaar.models.proxmox import *


router = APIRouter(
    prefix='/proxmox',
    tags=['proxmox']
)

@router.get('/nodes', response_model=List[Node])
async def list_nodes(
    proxmox: Annotated[ProxmoxAPI, Depends(proxmox)]
) -> List[Node]:
    return [ Node.model_validate(node) for node in proxmox.nodes.get() ]


async def __list_node_qemus(proxmox: ProxmoxAPI, node: Node) -> List[Qemu]:
    return [ Qemu.model_validate(qemu) for qemu in proxmox.nodes(node.node).get('qemu') ]

async def __virtual_machines(proxmox: ProxmoxAPI) -> List[VirtualMachine]:
    return [
        VirtualMachine.model_validate({'node': node, **(qemu.model_dump())})
        for node in (await list_nodes(proxmox))
        for qemu in (await __list_node_qemus(proxmox, node))
    ]

@router.get('/virtual_machines', response_model=List[VirtualMachine])
async def list_virtual_machines(proxmox: Annotated[ProxmoxAPI, Depends(proxmox)]) -> List[VirtualMachine]:
    return [
        vm
        for vm in (await __virtual_machines(proxmox))
        if vm.template is None
    ]

@router.get('/templates', response_model=List[VirtualMachine])
async def list_templates(proxmox: Annotated[ProxmoxAPI, Depends(proxmox)]) -> List[VirtualMachine]:
    return [
        vm
        for vm in (await __virtual_machines(proxmox))
        if vm.template is not None
    ]

async def __find_virtual_machine(proxmox: ProxmoxAPI, vmid: int) -> VirtualMachine | None:
    for vm in await __virtual_machines(proxmox):
        if vm.vmid == vmid: return vm
    return None

@router.post('/clone/{vmid}', response_model=TaskResult)
async def clone_virtual_machine(
    proxmox: Annotated[ProxmoxAPI, Depends(proxmox)], vmid: int, clone: QemuClone
) -> TaskResult:
    if (template := await __find_virtual_machine(proxmox, vmid)) is None:
        raise IndexError(vmid)
    
    task = proxmox.nodes(template.node.node).qemu(template.vmid).clone.create(**(clone.model_dump()))
    
    return Tasks.blocking_status(proxmox, task)

@router.delete('/virtual_machine/{vmid}', response_model=TaskResult)
async def delete_virtual_machine(
    proxmox: Annotated[ProxmoxAPI, Depends(proxmox)], vmid: int
) -> TaskResult:
    if (vm := await __find_virtual_machine(proxmox, vmid)) is None:
        raise IndexError(vmid)
    
    task = proxmox.nodes(vm.node.node).qemu(vm.vmid).delete()
    
    return Tasks.blocking_status(proxmox, task)