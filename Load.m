clc
clear
close

%%

for i=1:9
    x_train = zeros(0, 1000, 3);
    x_test = zeros(0, 1000, 3);
    y_train = zeros(0, 1);
    y_test = zeros(0, 1);
    trial = 0;
    for j=1:3
        file_name = strcat('B0', int2str(i), '0', int2str(j), 'T.gdf');
        [s, h] = sload(file_name);
        ar_select = 0;
        for k=1:length(h.EVENT.TYP)
            if h.EVENT.TYP(k)==769 || h.EVENT.TYP(k)==770
               ar_select = ar_select + 1; 
            end
            if h.EVENT.TYP(k)==769 || h.EVENT.TYP(k)==770 && h.EVENT.TYP(k-1)~=1023
               trial=trial+1;
               x_train(trial,:,:) = s(h.EVENT.POS(k):h.EVENT.POS(k)+1000-1, 1:3);
               y_train = [y_train; h.Classlabel(ar_select)];
            end
        end
    end
    
    trial = 0;
    for jj=4:5
        file_name = strcat('B0', int2str(i), '0', int2str(jj), 'E.gdf');
        [s, h] = sload(file_name);
        classlabel_name = strcat('B0', int2str(i), '0', int2str(jj), 'E.mat');
        load(classlabel_name)
        ar_select = 0;
        for k=1:length(h.EVENT.TYP)
            if h.EVENT.TYP(k)==783
               ar_select = ar_select + 1;
            end
            if h.EVENT.TYP(k)==783 && h.EVENT.TYP(k-1)~=1023
               trial=trial+1;
               x_test(trial,:,:) = s(h.EVENT.POS(k):h.EVENT.POS(k)+1000-1, 1:3);
               y_test = [y_test; classlabel(ar_select)];
            end
        end
    end
    
    [ind1, ind2, ind3] = find(isnan(x_train) == 1);
    index = zeros(0, 1);
    for ii=1:size(ind1, 1)
        if size(find(ind1(ii) == index), 1) == 0
            index = [index; ind1(ii)];
        end
    end
    x_train(index, :, :) = [];
    y_train(index, :) = [];
    
    
    [ind1, ind2, ind3] = find(isnan(x_test) == 1);
    index = zeros(0, 1);
    for ii=1:size(ind1, 1)
        if size(find(ind1(ii) == index), 1) == 0
            index = [index; ind1(ii)];
        end
    end
    x_test(index, :, :) = [];
    y_test(index, :) = [];    
    
    for jj=1:length(y_train)
        if y_train(jj)==2
           y_train(jj)=0;
        end
    end
    
    for j=1:length(y_test)
        if y_test(j)==2
           y_test(j)=0;
        end
    end
    
    name_to_save = strcat('sub', int2str(i));
    save(name_to_save, 'x_train', 'y_train', 'x_test', 'y_test')
end



