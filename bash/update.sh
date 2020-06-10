#!/bin/bash
#
# written by Hiyang @ 2016-12-19
# version: 1.2 @ 2016-12-19

#++++++++++++++++++++++++  Parameter Initializtion  ++++++++++++++++++++++++
ProjectName=
VersionCount=
Log=${ProjectName}.Log
ApacheUser=www
#----------------------  Parameter Initializtion END  ----------------------
Time=$(date +"%F-%H-%M")

#++++++++++++++++++++++++  Func Initializtion  ++++++++++++++++++++++++
ClearRuntime(){
    rm -rf $ProjectName/Runtime/* && echo -e "Clear Runtime OK.\n"
}

CheckRumtime(){
    [ ! -d $ProjectName/Runtime ] && mkdir $ProjectName/Runtime/
    chown -R $ApacheUser:$ApacheUser $ProjectName/Runtime/
}

Backup(){
    zip -r ${ProjectName}-$Time.zip $ProjectName &> /dev/null && echo -e "Backup OK.\n"
}

RecordLog(){
# 备份成功才记录日志，避免首次更新时就记录日志
    if ls ${ProjectName}-$Time.zip &> /dev/null; then
        echo "$Time" >> $Log
    fi
}

CheckProjectExist(){
    if [ ! -e $ProjectName ]; then
        update=first
    else
        update=later
    fi
}

CheckZipExist(){
    if [ ! -e $ProjectName.zip ]; then
        echo "There is no zip, please upload again."
        exit 1
    fi
}

CheckLog(){
    [ ! -e $Log ] && touch $Log
    BackupCount=$(wc -l $Log | cut -d" " -f 1)
    BackupCount=${BackupCount-0}
}

UnzipAndClearZip(){
    if unzip -o $ProjectName.zip &> /dev/null && echo -e "Unzip $ProjectName.zip OK.\n"; then
        rm -rf $ProjectName.zip && echo -e "Clear upload OK.\n"
    else
        echo "There is something wrong during unzip $ProjectName.zip"
        exit 2
    fi
}

BackupClear(){
	CheckLog
	# whether to rm old and keep n backup
    if [ $BackupCount -gt $VersionCount ]; then
        TO_RM=$ProjectName-$(head -n1 $Log).zip
	    rm -rf $TO_RM
	    sed -i "/$(head -n1 $Log)/d" $Log
	    echo -e "Backup check oK, \c"
        CheckLog
        echo "Now, you have $BackupCount backup."
    else
        echo "Now, you have $BackupCount backup."
	fi
}

Update(){
    CheckZipExist
    CheckProjectExist
	CheckLog
    clear
    # Tips before operations
    if [ $update == "first" ]; then
        printf "
        You're doing first updating:
        1 unzip.
            unzip -o $ProjectName.zip
        2 clear upload.
            rm -rf $ProjectName.zip
        "
        read -t 15 -p "do you want to continue?(y/n) " yn
        if [[ ! $yn =~ ^[y,n]$ ]]; then
            echo "Sorry, Error Input, Please Enter y/n."
            exit 1
        elif [ $yn = y ]; then
            # unzip and clear upload
            UnzipAndClearZip

            # RecordLog
            RecordLog
            # CheckRutime
            CheckRumtime
        else
            echo "You have do nothing right now."
        fi
    elif [ $update == "later" ]; then
        printf "
        You'll do following operations:
        1 delete Runtime before backup.
            rm -rf $ProjectName/Runtime/*
        2 backup.
            zip -r ${ProjectName}-$Time.zip $ProjectName
        3 unzip.
            unzip -o $ProjectName.zip
        4 clear upload.
            rm -rf $ProjectName.zip
        5 make sure old backup is less than $VersionCount.
            Now, BackupCount is $BackupCount.\n
        "
        read -t 15 -p "do you want to continue?(y/n) " yn
        if [[ ! $yn =~ ^[y,n]$ ]]; then
            echo "Sorry, Error Input, Please Enter y/n."
            exit 1
        elif [ $yn = y ]; then
            # clear Runtime
            ClearRuntime

            # backup
            Backup

            # unzip and clear upload
            UnzipAndClearZip

            # RecordLog
            RecordLog

            # CheckBackup
            BackupClear

        else
            echo "You have do nothing right now."
        fi
    else
        echo "There is something wrong!"
    fi
}

BackupOnly(){
	CheckLog
    clear
    # Tips before operations
    printf "
    You'll do following operations:
    1 backup.
        zip -r ${ProjectName}-$Time.zip $ProjectName
    2 make sure old backup is less than $VersionCount.
        Now, BackupCount is $BackupCount.\n
    "
    read -t 15 -p "do you want to continue?(y/n) " yn
    if [[ ! $yn =~ ^[y,n]$ ]]; then
        echo "Sorry, Error Input, Please Enter y/n."
    elif [ $yn = y ]; then
        Backup
        RecordLog
        BackupClear
    else
        echo "You have do nothing right now."
        exit 1
    fi
}

Usage(){
echo "The script usage:
    <> bash update --update     --> update
    <> bash update --backup     --> backup only
    <> bash update --check      --> check only"
}
#----------------------  Func Initializtion END  ----------------------

case $1 in
    --update)
        Update;;
    --backup)
        BackupOnly;;
    --check)
        BackupClear;;
    --help)
        Usage;;
    *)
        echo "Error input"
        exit 2;;
esac
