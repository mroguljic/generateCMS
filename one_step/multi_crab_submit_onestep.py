import os

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', type=str, default='HbbGamma_JHUGen_pythia8', help='name of dataset')
    parser.add_argument('--config', type=str, default='Hbb_fragment',  help='config of dataset')
    parser.add_argument('--eosdir', type=str, default='/store/group/phys_b2g/mrogulji/Hgamma_HToBB/one_step', help='eosdir')
    parser.add_argument('--site', type=str, default='T2_CH_CERN', help='site')
    parser.add_argument('--begin-seed', type=int, default=0, help='begin seed, should be between 0 and 99')
    args = parser.parse_args()

    from CRABAPI.RawCommand import crabCommand
    from CRABClient.ClientExceptions import ClientException
    from httplib import HTTPException

    from WMCore.Configuration import Configuration
    config = Configuration()

    config.section_("General")
    config.General.workArea = 'crab'
    config.General.transferOutputs = True
    config.General.transferLogs = False

    config.section_("JobType")
    config.JobType.pluginName = 'PrivateMC'

    config.section_("Data")
    nevent = 1000
    config.Data.inputDBS = 'global'
    config.Data.splitting = 'EventBased'
    config.Data.unitsPerJob = nevent
    #config.Data.totalUnits = 10000
    config.Data.totalUnits = 5 # for testing
    config.Data.publication = True
    config.Data.allowNonValidInputDataset = True

    config.section_("Site")
    config.Site.storageSite = args.site
    # We want to put all the CRAB project directories from the tasks we submit here into one common directory.
    # That's why we need to set this parameter (here or above in the configuration file, it does not matter, we will not overwrite it).

    def submit(config):
        try:
            crabCommand('submit', config = config)
        except HTTPException as hte:
            print("Failed submitting task: %s" % (hte.headers))
        except ClientException as cle:
            print("Failed submitting task: %s" % (cle))

    #############################################################################################
    ## From now on that's what users should modify: this is the a-la-CRAB2 configuration part. ##
    #############################################################################################
    pset_dir = os.environ["CMSSW_BASE"]+"/src"
    config.General.requestName = 'Private_'+args.name+'_ONESTEP'
    config.Data.outputDatasetTag = 'PrivateMC'
    config.Data.outputPrimaryDataset = args.name
    config.Data.outLFNDirBase = args.eosdir + args.name
    config.JobType.allowUndistributedCMSSW = True
    #config.JobType.psetName = 'FAKEMiniAODv2_cfg.py'
    config.JobType.psetName = 'FAKENanoAODv9_cfg.py'
    config.JobType.inputFiles = ['FrameworkJobReport.xml', 'inputs', 'gammaHiggs0MyyTobb_M125_13TeV_JHUGenV750_pythia8_slc7_amd64_gcc820_CMSSW_10_6_0.tgz']
    config.JobType.maxMemoryMB = 5000
    config.JobType.numCores = 1
    config.JobType.sendExternalFolder = True
    config.JobType.scriptArgs = ['nevent=%i'%nevent, 'nthread=1', 'procname=%s'%args.config, 'beginseed=%i'%args.begin_seed]  
    config.JobType.scriptExe = 'exe.sh'

    print('config %s' %(config.JobType.psetName))
    print('output %s' %(config.Data.outLFNDirBase))
    submit(config)
        
