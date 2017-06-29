# BSP support for ARM64
from build_rts_support.bsp import BSP
from build_rts_support.target import DFBBTarget


class Aarch64Arch(BSP):
    @property
    def name(self):
        return "aarch64"

    def __init__(self):
        super(Aarch64Arch, self).__init__()
        self.add_sources('arch', [
            'src/i-aarch64.ads', 'src/i-aarch64.adb',
            'src/i-cache/i-cache.ads',
            'src/i-cache/aarch64/i-cache.adb'])
        self.add_sources('gnarl', [
            'src/s-bbcpsp/aarch64/s-bbcpsp.ads',
            'src/s-bbcppr/new/s-bbcppr.ads',
            'src/s-bbcppr/aarch64/s-bbcppr.adb',
            'aarch64/context_switch.S',
            'src/s-bbinte/generic/s-bbinte.adb'])


class Aarch64Target(DFBBTarget):
    @property
    def target(self):
        return 'aarch64-elf'

    @property
    def parent(self):
        return Aarch64Arch

    @property
    def has_newlib(self):
        return True

    @property
    def has_timer_64(self):
        return True

    @property
    def zfp_system_ads(self):
        return 'system-xi-aarch64.ads'

    @property
    def sfp_system_ads(self):
        return 'system-xi-arm-sfp.ads'

    @property
    def full_system_ads(self):
        return 'system-xi-arm-full.ads'

    def amend_rts(self, rts_profile, cfg):
        super(Aarch64Target, self).amend_rts(rts_profile, cfg)
        if rts_profile == 'ravenscar-full':
            cfg.rts_xml = cfg.rts_xml.replace(
                '"-nostartfiles"',
                ('"-u", "_Unwind_Find_FDE", "-Wl,--eh-frame-hdr",\n'
                 '        "-nostartfiles"'))


class AARCH64QEMU(Aarch64Target):
    @property
    def name(self):
        return "qemu"

    @property
    def parent(self):
        return Aarch64Arch

    @property
    def loaders(self):
        return ('RAM', 'MCPART')

    @property
    def sfp_system_ads(self):
        # Only zfp support for now. To be removed when ravenscar-sfp is in
        return None

    @property
    def full_system_ads(self):
        # Only zfp support for now. To be removed when ravenscar-sfp is in
        return None

    @property
    def compiler_switches(self):
        # The required compiler switches
        return ('-mlittle-endian', '-mcpu=cortex-a53')

    def __init__(self):
        super(AARCH64QEMU, self).__init__(
            mem_routines=True,
            small_mem=False)

        self.add_linker_script('aarch64/qemu/ram.ld', loader='RAM')
        self.add_linker_script('aarch64/qemu/mcpart.ld', loader='MCPART')
        self.add_sources('crt0', [
            'aarch64/qemu/start-ram.S',
            'aarch64/qemu/start-part.S',
            'src/s-textio/zynq/s-textio.adb',
            'src/s-macres/zynq/s-macres.adb'])


class ZynqMP(Aarch64Target):
    @property
    def name(self):
        return "zynqmp"

    @property
    def parent(self):
        return Aarch64Arch

    @property
    def readme_file(self):
        return 'aarch64/zynqmp/README'

    @property
    def loaders(self):
        return ('RAM', )

    @property
    def system_ads(self):
        return {'zfp': self.zfp_system_ads,
                'ravenscar-sfp': 'system-xi-aarch64-sfp.ads',
                'ravenscar-mc': 'system-xi-aarch64-sfp.ads',
                'ravenscar-full': 'system-xi-aarch64-full.ads'}

    @property
    def compiler_switches(self):
        # The required compiler switches
        return ('-mlittle-endian', '-mcpu=cortex-a53')

    def amend_rts(self, rts_profile, cfg):
        super(ZynqMP, self).amend_rts(rts_profile, cfg)
        if rts_profile == 'ravenscar-mc':
            cfg.add_sources('arch', {
                'start-config.h': 'aarch64/zynqmp/start-config-el2.h',
                'memmap.s': 'aarch64/zynqmp/memmap-el2.s'})
            cfg.add_sources('gnarl', [
                'src/s-bbpara/zynqmp-el2/s-bbpara.ads'])
        else:
            cfg.add_sources('arch', {
                'start-config.h': 'aarch64/zynqmp/start-config-el1.h',
                'memmap.s': 'aarch64/zynqmp/memmap-el1.s'})
            cfg.add_sources('gnarl', [
                'src/s-bbpara/zynqmp/s-bbpara.ads'])

    def __init__(self):
        super(ZynqMP, self).__init__(
            mem_routines=True,
            small_mem=False)

        self.add_linker_script('aarch64/zynqmp/ram.ld', loader=None)
        self.add_sources('crt0', [
            'aarch64/zynqmp/start-ram.S',
            'aarch64/zynqmp/trap_vector.S',
            'src/aarch64/trap_dump.ads',
            'src/aarch64/trap_dump.adb',
            'src/s-textio/zynqmp/s-textio.adb',
            'src/s-macres/zynqmp/s-macres.adb'])
        self.add_sources('gnarl', [
            'src/a-intnam/zynqmp/a-intnam.ads',
            'src/s-bbbosu/armv8a/s-bbbosu.adb'])


class Rpi3Base(Aarch64Target):
    @property
    def loaders(self):
        return ('RAM', )

    @property
    def compiler_switches(self):
        # The required compiler switches
        return ('-mlittle-endian', '-mcpu=cortex-a53')

    @property
    def readme_file(self):
        return 'arm/rpi2/README'

    def __init__(self):
        super(Rpi3Base, self).__init__(
            mem_routines=True,
            small_mem=False)

        self.add_linker_script('aarch64/rpi3/ram.ld', loader='RAM')
        self.add_sources('crt0', [
            'src/i-raspberry_pi.ads',
            'src/aarch64/trap_dump.ads',
            'src/aarch64/trap_dump.adb',
            'src/s-textio/rpi2-mini/s-textio.adb',
            'src/s-macres/rpi2/s-macres.adb'])
        self.add_sources('gnarl', [
            'src/a-intnam/rpi2/a-intnam.ads',
            'src/s-bbpara/rpi2/s-bbpara.ads',
            'src/s-bbbosu/rpi3/s-bbbosu.adb'])


class Rpi3(Rpi3Base):
    @property
    def name(self):
        return "rpi3"

    def __init__(self):
        super(Rpi3, self).__init__()

        self.add_sources('crt0', [
            'aarch64/rpi3/start-ram.S',
            'aarch64/rpi3/memmap.s',
            'src/s-textio/rpi2-mini/s-textio.adb'])
        self.add_sources('gnarl', [
            'src/s-bbpara/rpi2/s-bbpara.ads'])


class Rpi3Mc(Rpi3Base):
    @property
    def name(self):
        return "rpi3mc"

    def __init__(self):
        super(Rpi3Mc, self).__init__()

        self.add_sources('crt0', [
            'aarch64/rpi3-mc/start-ram.S',
            'aarch64/rpi3-mc/traps_el3.S',
            'aarch64/rpi3-mc/traps_el2cur.S',
            'aarch64/rpi3-mc/traps_el2low.S',
            'aarch64/rpi3-mc/traps_common.h',
            'aarch64/rpi3-mc/memmap.s',
            'src/s-textio/rpi2-pl011/s-textio.adb'])
        self.add_sources('gnarl', [
            'src/s-bbpara/rpi2-hyp/s-bbpara.ads'])
